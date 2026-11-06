# Copyright (c) 2026 Mohamed Gaber
# SPDX-License-Identifier: BSD-3-Clause
import gzip
import re
import shutil
import subprocess
import sys
import sysconfig
from pathlib import Path

import yaml
from wheel.wheelfile import WheelFile

__repo_root__ = Path(__file__).resolve().parents[1]

MACOSX_MINIMUM_TARGET = 15


def get_platform_tag():
    PLATFORM_TAG_RAW = sysconfig.get_platform()
    if sys.platform == "darwin":
        PLATFORM_TAG_RAW = PLATFORM_TAG_RAW.replace(
            "universal2", "arm64"
        )  # confuses delocate
        target = f"{MACOSX_MINIMUM_TARGET}.0"
        PLATFORM_TAG_RAW = re.sub(
            r"(macosx)-\d+\.\d+", rf"\1-{target}", PLATFORM_TAG_RAW
        )
    # Source for these substitutions:
    # 	https://github.com/pypa/wheel/blob/197012dcb8a9da10570d6486bc1a70305861e7f2/src/wheel/_bdist_wheel.py#L351
    return (
        PLATFORM_TAG_RAW.lower().replace("-", "_").replace(".", "_").replace(" ", "_")
    )


def build(git_repo):
    git_repo = Path(git_repo)

    # 1. Get Version
    describe = subprocess.check_output(
        ["git", "describe", "--long"],
        encoding="utf8",
        stderr=subprocess.PIPE,
        cwd=git_repo,
    ).strip()

    tag, commit_count, _ = describe.rsplit("-", maxsplit=2)

    wheel_ver = f"{tag}"
    if int(commit_count) > 0:
        wheel_ver += (
            f".{commit_count}"  # not .post because we want .post for our own purposes
        )
    if "Q" in wheel_ver:
        wheel_ver = wheel_ver.replace("Q", ".")

    with open(__repo_root__ / "openroad_version.yml", encoding="utf8") as f:
        repo_info = yaml.safe_load(f)

    post = repo_info["post"]
    if post > 0:
        wheel_ver += f".post{post}"

    def is_canonical(version):
        return (
            re.match(
                r"^([1-9][0-9]*!)?(0|[1-9][0-9]*)(\.(0|[1-9][0-9]*))*((a|b|rc)(0|[1-9][0-9]*))?(\.post(0|[1-9][0-9]*))?(\.dev(0|[1-9][0-9]*))?$",
                version,
            )
            is not None
        )

    if not is_canonical(wheel_ver):
        print(f"Generated invalid version: {wheel_ver}", file=sys.stderr)
        sys.exit(1)

    platform = get_platform_tag()

    print(f"Building {wheel_ver} for {platform}...", file=sys.stderr)

    # 2. Reset state and apply patches
    subprocess.check_call(
        ["git", "reset", "--hard", "HEAD"],
        encoding="utf8",
        stderr=subprocess.PIPE,
        cwd=git_repo,
    )

    for patch in (__repo_root__ / "patches").glob("*"):
        subprocess.check_call(
            ["git", "apply", str(patch)],
            encoding="utf8",
            cwd=git_repo,
        )

    subprocess.check_call(
        [
            "perl",
            "-i",
            "-p",
            "-e",
            r's/homepage\s*=\s*"(.+)"/homepage = "https\:\/\/github.com\/donn\/ord-wheels"/;',
            "-e",
            r's/distribution\s*=\s*"([A-Za-z\d\._\-]+)"/distribution = "openroad"/;',
            "-e",
            rf's/version\s*=\s*"([A-Za-z\d\._\-]+)"/version = "{wheel_ver}"/;',
            "-e",
            rf's/platform\s*=\s*"([A-Za-z\d\._\-]+)"/platform = "{platform}"/;',
            str(git_repo / "python" / "openroad" / "BUILD"),
        ]
    )

    bazel_args = ["--config=release"]
    if sys.platform == "darwin":
        bazel_args.extend(("--macos_minimum_os", str(MACOSX_MINIMUM_TARGET)))

    # 3. Build wheel and binary
    subprocess.check_call(
        [
            "bazel",
            "build",
            *bazel_args,
            "//python/openroad:openroad_wheel",
        ],
        cwd=git_repo,
    )

    subprocess.check_call(
        [
            "bazel",
            "build",
            *bazel_args,
            "//:openroad",
        ],
        cwd=git_repo,
    )

    # 3. Copy over wheel and binary for further processing
    base_wheel_path = next(
        (git_repo / "bazel-bin" / "python" / "openroad").glob("*.whl")
    )

    dist_staging_dir = __repo_root__ / "dist_staging"
    dist_staging_dir.mkdir(parents=True, exist_ok=True)

    ord_bin_dir = __repo_root__ / "base_dir" / "openroad_bin"

    wheel_path_prerepair = dist_staging_dir / base_wheel_path.name

    shutil.copyfile(base_wheel_path, wheel_path_prerepair)

    base_bin_path = git_repo / "bazel-bin" / "openroad"

    bin_path = ord_bin_dir / "openroad.gz"

    with gzip.open(bin_path, "w") as f_out, open(base_bin_path, "rb") as f_in:
        f_out.write(f_in.read())

    # 4. update wheel
    with WheelFile(wheel_path_prerepair, "r") as wf:
        metadata = wf.read(wf.dist_info_path + "/METADATA").decode("utf8")

    with WheelFile(wheel_path_prerepair, "a") as wf:
        wf.write_files("base_dir")
        wf.write("entry_points.txt", wf.dist_info_path + "/entry_points.txt")

        metadata_new = ""
        for line in metadata.splitlines():
            if line.strip() == "":
                metadata_new += "License-Expression: GPLv3\n\n"
                metadata_new += (__repo_root__ / "README.md").read_text()
                metadata_new += "\n"
                break
            metadata_new += line
            metadata_new += "\n"
        wf.writestr(wf.dist_info_path + "/METADATA", metadata_new)

    # 5. repair/delocate wheel
    if sys.platform == "darwin":
        subprocess.check_call(
            ["delocate-wheel", str(wheel_path_prerepair), "-w", "dist"],
            encoding="utf8",
        )
    elif sys.platform == "linux":
        subprocess.check_call(
            ["auditwheel", "repair", str(wheel_path_prerepair), "-w", "dist"],
            encoding="utf8",
        )

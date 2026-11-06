# Copyright (c) 2026 Mohamed Gaber
# SPDX-License-Identifier: BSD-3-Clause
import gzip
import os
import sys
from pathlib import Path

__here__ = Path(__file__).resolve().parent


def openroad():
    extracted = __here__ / "openroad"
    if not extracted.is_file():
        gzipped = __here__ / "openroad.gz"
        if not gzipped.is_file():
            print(
                "Error: Compressed OpenROAD binary not found. Try reinstalling the wheel. Exiting.",
                file=sys.stderr,
            )
            sys.exit(1)
        print(
            "Performing first-time extraction for OpenROAD binary...", file=sys.stderr
        )
        with gzip.open(gzipped) as f_in, open(extracted, "wb") as f_out:
            f_out.write(f_in.read())
        os.chmod(extracted, 0o555)

    os.execlp(extracted, "openroad", *sys.argv[1:])


if __name__ == "__main__":
    openroad()

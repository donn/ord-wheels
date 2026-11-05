import argparse

from . import build

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("git_repo")
    ns = ap.parse_args()
    build(**ns.__dict__)

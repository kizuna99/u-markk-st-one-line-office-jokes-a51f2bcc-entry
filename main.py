#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Write the one-line office joke to /output/entry.txt (make.fun program/v1)."""
import os

JOKE = (
    "My boss said 'circle back' so often that our Monday meeting "
    "achieved orbit and is now officially a satellite."
)


def main() -> None:
    out_path = os.environ.get("OUTPUT_PATH", "/output/entry.txt")
    directory = os.path.dirname(out_path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="") as fh:
        fh.write(JOKE)


if __name__ == "__main__":
    main()

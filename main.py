# SPDX-License-Identifier: MIT
"""One-Line Office Jokes — entry program (harness program/v1).

Writes a single one-line office joke to /output/entry.txt.
The gate requires UTF-8 text of 1 to 199 characters, not only
whitespace, on a single line. This entry emits no trailing newline,
which also keeps its byte count as small as the text itself allows.
"""

import os
import sys
from pathlib import Path

# The joke itself: a real office detail ("circle back", the Monday
# meeting) with the laugh saved for the very last word.
JOKE = (
    "My boss said 'circle back' so often that our Monday meeting "
    "achieved orbit and is now officially a satellite."
)

# Gate limits from the competition rules.
MIN_CHARS = 1
MAX_CHARS = 199

DEFAULT_OUTPUT = "/output/entry.txt"


def build_text() -> str:
    """Return the entry text exactly as it should appear on disk."""
    return JOKE


def validate(text: str) -> None:
    """Raise ValueError if *text* would fail the output gate."""
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        raise ValueError(f"text length {len(text)} outside {MIN_CHARS}-{MAX_CHARS}")
    if not text.strip():
        raise ValueError("text is only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("text must be a single line")


def verify_round_trip(target: Path, payload: bytes) -> None:
    """Read the written file back and assert it survived intact.

    Catches silent truncation or newline translation by the storage
    layer: what the gate will read must be byte-for-byte what we meant
    to write, and it must still satisfy the gate limits on re-reading.
    """
    on_disk = target.read_bytes()
    if on_disk != payload:
        raise IOError(f"round-trip mismatch: wrote {len(payload)} bytes, "
                      f"read back {len(on_disk)}")
    validate(on_disk.decode("utf-8"))


def main() -> int:
    text = build_text()
    validate(text)
    target = Path(os.environ.get("OUTPUT_PATH", DEFAULT_OUTPUT))
    target.parent.mkdir(parents=True, exist_ok=True)
    # Bytes, not text mode: guarantees UTF-8 and no trailing newline
    # is added or translated by the platform's newline handling.
    payload = text.encode("utf-8")
    target.write_bytes(payload)
    verify_round_trip(target, payload)
    return 0


if __name__ == "__main__":
    sys.exit(main())

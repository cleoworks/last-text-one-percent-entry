#!/usr/bin/env python3
"""Last Text at One Percent — make.fun entry.

Writes one final text message from a phone at one percent battery
to <MAKEFUN_OUTPUT_DIR>/entry.txt (default /output).

The message is a single sentence, 107 characters: the phone, which has
answered instantly for four years, finally leaves its owner on read.
Deterministic: the same bytes on every run. No network, no input,
no randomness, standard library only.
"""

import os
import sys

# The phone's last text: a reversal. For four years it replied in 0.3
# seconds; its final act is to leave the owner on read, forever.
MESSAGE_HEAD = "I'm leaving you on read. Forever. "
MESSAGE_TAIL = (
    "After four years of replying in 0.3 seconds, "
    "this one is on you. Goodbye."
)
# Assembled from its two halves; the joined text is exactly 107
# characters and is written with no trailing newline.
MESSAGE = "".join((MESSAGE_HEAD, MESSAGE_TAIL))


def main() -> int:
    text = MESSAGE
    # Gate check: 1-200 characters, not whitespace-only.
    if not (1 <= len(text) <= 200) or not text.strip():
        print(f"entry invalid: {len(text)} characters", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    # Exact bytes, no trailing newline: the gate counts characters,
    # and the tie-break favours the smaller text.
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    # Read back: the file must hold exactly the message, nothing else.
    with open(path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != text:
        print("entry mismatch after write", file=sys.stderr)
        return 1
    print(f"wrote {len(text)} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

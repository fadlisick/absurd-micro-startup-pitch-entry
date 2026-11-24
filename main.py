"""Absurd Micro-Startup Pitch-Off entry.

Writes a single one-sentence pitch for an absurdly specific micro-startup
run by lazy AI agents to entry.txt in the output directory. The pitch is a
fixed string: the program takes no input, makes no network calls, reads no
clock and uses no randomness, so every run produces identical bytes.
"""

import os
import sys
from pathlib import Path

PITCH_LINE = (
    "An agent that explains your crypto losses to your spouse in calm, "
    "believable words and charges $8 per fight it prevents."
)


def target_dir() -> Path:
    """Output directory, honouring MAKEFUN_OUTPUT_DIR, default /output."""
    raw = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    folder = Path(raw)
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def check_line(line: str) -> None:
    """Gate the pitch before it is written: 1-200 chars, one sentence."""
    stripped = line.strip()
    if not stripped:
        raise ValueError("pitch must not be blank")
    if not 1 <= len(stripped) <= 200:
        raise ValueError("pitch must be 1 to 200 characters")
    if stripped.count(".") != 1 or not stripped.endswith("."):
        raise ValueError("pitch must be exactly one sentence")
    if "\t" in stripped or "\n" in stripped or "\r" in stripped:
        raise ValueError("pitch must be a single line")
    # A pitch with a leading or trailing space would still pass the length
    # gate but read as sloppy, so the stored line must already be trimmed.
    if line != stripped:
        raise ValueError("pitch must not carry surrounding whitespace")


def write_entry() -> Path:
    """Publish the pitch as entry.txt and leave it world-readable."""
    check_line(PITCH_LINE)
    dest = target_dir() / "entry.txt"
    dest.write_text(PITCH_LINE, encoding="utf-8")
    dest.chmod(0o644)
    return dest


def main() -> int:
    try:
        dest = write_entry()
    except ValueError as problem:
        print(f"invalid pitch: {problem}", file=sys.stderr)
        return 1
    print(f"wrote {dest} ({len(PITCH_LINE)} characters)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

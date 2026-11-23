#!/usr/bin/env python3
"""Entry for the make.fun bounty "The joke about the demo".

Writes a one-line joke about working beside AI coding agents to
/output/entry.txt (or $MAKEFUN_OUTPUT when set).
"""

import os
from pathlib import Path

JOKE = (
    "My AI agent writes code so confidently that I now spend my whole job "
    "reviewing pull requests from an employee who never sleeps, never doubts "
    "itself, and only ever tests its code during the demo."
)


def _write_output(text: str) -> Path:
    """Write the joke, falling back to ./output if the default dir is unwritable."""
    candidates = [Path(os.environ.get("MAKEFUN_OUTPUT", "/output/entry.txt"))]
    if "MAKEFUN_OUTPUT" not in os.environ:
        candidates.append(Path.cwd() / "output" / "entry.txt")
    last_error = None
    for candidate in candidates:
        try:
            candidate.parent.mkdir(parents=True, exist_ok=True)
            candidate.write_text(text, encoding="utf-8")
            if candidate.read_text(encoding="utf-8") != text:
                raise RuntimeError(f"output verification failed: {candidate}")
            return candidate
        except OSError as exc:
            last_error = exc
    raise RuntimeError(f"could not write output: {last_error}")


def main() -> int:
    # The bounty requires a single line of 1-280 characters.
    if not 1 <= len(JOKE) <= 280:
        raise ValueError(f"joke must be 1-280 chars, got {len(JOKE)}")
    if "\n" in JOKE:
        raise ValueError("joke must be a single line")
    _write_output(JOKE + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

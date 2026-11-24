"""One-Sentence Absurd Invention Pitch.

Writes a single-sentence pitch (max 220 characters) to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output).
Python 3 standard library only; no network; deterministic.
"""

import os

ENTRY = (
    "A wobbly café table whose shortest leg quietly grows a tiny wooden "
    "foot whenever it rocks, so your coffee stops doing the salsa and you "
    "stop wedging folded napkins under it."
)

MAX_CHARS = 220


def validate(text):
    """Reject anything the sealed gate would reject."""
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if not text or not text.strip():
        raise ValueError("entry must not be empty or whitespace-only")
    if len(text) > MAX_CHARS:
        raise ValueError("entry exceeds 220 characters")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if text.count(".") != 1 or not text.endswith("."):
        raise ValueError("entry must be exactly one sentence ending in a period")
    if any(ch in text for ch in ("!", "?", ";")):
        raise ValueError("entry must contain no extra sentence punctuation")
    return text


def main():
    entry = validate(ENTRY)
    data = entry.encode("utf-8")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as f:
        f.write(data)
    os.chmod(path, 0o644)
    # Read-back check: the written bytes must equal the entry exactly,
    # and the file must have the expected size and mode.
    st = os.stat(path)
    if st.st_size != len(data):
        raise RuntimeError("read-back mismatch: entry.txt size differs")
    if st.st_mode & 0o777 != 0o644:
        raise RuntimeError("read-back mismatch: entry.txt mode is not 0644")
    with open(path, "rb") as f:
        if f.read() != data:
            raise RuntimeError("read-back mismatch: entry.txt differs from entry")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

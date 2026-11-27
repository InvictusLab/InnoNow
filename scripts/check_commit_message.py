"""Validate a commit message file, or read its exact bytes from stdin with '-'."""

import re
import sys
import unicodedata
from pathlib import Path

TYPES = [
    "feat",
    "fix",
    "docs",
    "style",
    "refactor",
    "perf",
    "test",
    "build",
    "ci",
    "chore",
    "revert",
]
SCOPES = [
    "auth",
    "users",
    "items",
    "ui",
    "email",
    "api",
    "db",
    "deploy",
    "docs",
    "deps",
    "ci",
    "tooling",
    "agents",
    "innonow",
]
EXAMPLE = "fix(auth): reject expired password reset tokens"


def validate(message: bytes) -> None:
    if message.endswith(b"\n"):
        message = message[:-1].removesuffix(b"\r")
    if b"\r" in message or b"\n" in message:
        raise ValueError("Use a single line with an optional final LF or CRLF.")
    text = message.decode("utf-8")
    match = re.fullmatch(r"([a-z]+)\(([a-z]+)\): (.+)", text)
    if not match:
        raise ValueError(f"Expected <type>(<scope>): <subject>, e.g. {EXAMPLE}")
    commit_type, scope, subject = match.groups()
    if commit_type not in TYPES:
        raise ValueError(
            f"Unknown type '{commit_type}'. Choose from {', '.join(TYPES)}."
        )
    if scope not in SCOPES:
        raise ValueError(f"Unknown scope '{scope}'. Choose from {', '.join(SCOPES)}.")
    if subject != subject.strip() or not subject.isprintable():
        raise ValueError("Remove surrounding whitespace and control characters.")
    letters = [char for char in subject if char.isalpha()]
    if not letters or any(
        "LATIN" not in unicodedata.name(char, "") for char in letters
    ):
        raise ValueError("Write the subject in English.")
    if re.search(
        r"`[^`]+`|\[[^\]]*\]\([^)]+\)|(?<!\w)(\*{1,3})\S[^*]*?\1(?!\w)", subject
    ):
        raise ValueError("Use plain text for the subject. Remove Markdown formatting.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: check_commit_message.py <message-file|->")
    try:
        source = sys.argv[1]
        validate(
            sys.stdin.buffer.read() if source == "-" else Path(source).read_bytes()
        )
    except (OSError, ValueError) as error:
        sys.exit(f"Invalid commit message: {error}")

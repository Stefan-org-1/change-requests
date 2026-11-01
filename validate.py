"""Check every change file. Exit non-zero on the first bad file."""

import pathlib
import re
import sys
from datetime import datetime, timedelta

import yaml

MAX_WINDOW = timedelta(days=14)
MAX_EMERGENCY_WINDOW = timedelta(hours=24)
REQUIRED = {"repo", "version", "environments", "window", "reason", "emergency", "requested_by", "approvers"}


def as_time(v) -> datetime:
    t = v if isinstance(v, datetime) else datetime.fromisoformat(str(v))
    if t.tzinfo is None:
        raise ValueError(f"{v} has no timezone")
    return t


def check(path: pathlib.Path) -> list[str]:
    d = yaml.safe_load(path.read_text())
    if not isinstance(d, dict):
        return ["not a mapping"]
    errors = [f"missing {k}" for k in sorted(REQUIRED - d.keys())]
    errors += [f"unknown field {k}" for k in sorted(d.keys() - REQUIRED)]
    if errors:
        return errors
    if path.parent.name != d["repo"]:
        errors.append(f"repo is {d['repo']} but the file is under changes/{path.parent.name}/")
    if not re.fullmatch(r"[0-9a-f]{40}", str(d["version"])):
        errors.append("version must be a full 40-character commit SHA")
    if not d["environments"] or not all(isinstance(e, str) for e in d["environments"]):
        errors.append("environments must be a non-empty list of names")
    if not isinstance(d["emergency"], bool):
        errors.append("emergency must be true or false")
    if not isinstance(d["requested_by"], str) or not d["requested_by"].strip():
        errors.append("requested_by must be a GitHub login")
    if not isinstance(d["approvers"], list) or not all(isinstance(a, str) for a in d["approvers"]):
        errors.append("approvers must be a list of GitHub logins")
    if not str(d["reason"]).strip():
        errors.append("reason must not be empty")
    try:
        start, end = as_time(d["window"]["start"]), as_time(d["window"]["end"])
        limit = MAX_EMERGENCY_WINDOW if d["emergency"] is True else MAX_WINDOW
        if end <= start:
            errors.append("window end must be after start")
        elif end - start > limit:
            errors.append(f"window is longer than {limit}")
    except (KeyError, TypeError, ValueError) as e:
        errors.append(f"bad window: {e}")
    return errors


def main(root: str) -> int:
    bad = 0
    for path in sorted(pathlib.Path(root, "changes").glob("*/*.yaml")):
        for e in check(path):
            print(f"{path}: {e}")
            bad += 1
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "."))

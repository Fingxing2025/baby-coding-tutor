#!/usr/bin/env python3
"""Small local distribution helpers; no model, network, or learning database."""
import argparse
from pathlib import Path
import shutil
import sys
from zipfile import BadZipFile, ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "baby-coding-tutor"
NAME = "baby-coding-tutor"
VERSION = "0.1.0"
SCENARIOS = {"1": "01-todo", "2": "02-campus-board", "3": "03-reading-debug"}


def files_under(directory):
    result = {}
    for path in sorted(directory.rglob("*")):
        if "__pycache__" in path.parts or path.name in {".DS_Store"}:
            continue
        if path.is_file():
            result[path.relative_to(directory).as_posix()] = path.read_bytes()
    return result


def copy_skill(destination):
    """Never replace existing, different local instructions."""
    destination = Path(destination).expanduser()
    if destination.exists() or destination.is_symlink():
        if destination.is_dir() and files_under(destination) == files_under(SKILL):
            print(f"Already identical: {destination}")
            return destination
        raise ValueError(f"Existing destination differs; nothing overwritten: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SKILL, destination, ignore=shutil.ignore_patterns("__pycache__", ".DS_Store"))
    print(f"Installed: {destination}")
    return destination


def install(project=None, user=False):
    if user:
        base = Path.home()
    else:
        base = Path(project).expanduser().resolve()
        if not base.is_dir():
            raise ValueError(f"Project directory must already exist: {base}")
    return copy_skill(base / ".agents" / "skills" / NAME)


def prepare(number, destination):
    destination = Path(destination).expanduser().absolute()
    if destination.exists() or destination.is_symlink():
        raise ValueError(f"Choose a new test directory; nothing overwritten: {destination}")
    scenario = ROOT / "tests" / "projects" / SCENARIOS[number]
    destination.mkdir(parents=True)
    (destination / "TASK.md").write_bytes((scenario / "TASK.md").read_bytes())
    fixture = scenario / "fixture"
    if fixture.is_dir():
        for relative, content in files_under(fixture).items():
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
    copy_skill(destination / ".agents" / "skills" / NAME)
    print(f"Prepared Test {number}: {destination}")
    print("Open this folder in your coding agent, then send the prompt in TASK.md.")
    return destination


def package(destination=None):
    destination = Path(destination or ROOT / "dist" / f"{NAME}-v{VERSION}.zip").expanduser()
    if destination.exists() or destination.is_symlink():
        # Allow repeatable generation only for an unchanged archive.
        try:
            with ZipFile(destination) as archive:
                expected = {f"{NAME}/{p}": b for p, b in files_under(SKILL).items()}
                actual = {p: archive.read(p) for p in archive.namelist()}
        except (BadZipFile, OSError, ValueError) as error:
            raise ValueError(f"Cannot compare existing archive: {destination}") from error
        if expected == actual:
            print(f"Already identical: {destination}")
            return destination
        raise ValueError(f"Existing archive differs; choose a new --output: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(destination, "w", compression=ZIP_DEFLATED) as archive:
        for relative, content in files_under(SKILL).items():
            archive.writestr(f"{NAME}/{relative}", content)
    print(f"Packaged: {destination}")
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    install_parser = commands.add_parser("install", help="Copy skill without overwriting different files")
    scope = install_parser.add_mutually_exclusive_group(required=True)
    scope.add_argument("--project", help="Existing project directory")
    scope.add_argument("--user", action="store_true", help="Use ~/.agents/skills")
    prepare_parser = commands.add_parser("prepare", help="Create an isolated project test workspace")
    prepare_parser.add_argument("number", choices=SCENARIOS)
    prepare_parser.add_argument("--dest", required=True, help="A directory that does not exist yet")
    package_parser = commands.add_parser("package", help="Create one top-level skill folder ZIP")
    package_parser.add_argument("--output", help="Optional new archive path")
    args = parser.parse_args()
    try:
        if args.command == "install":
            install(args.project, args.user)
        elif args.command == "prepare":
            prepare(args.number, args.dest)
        else:
            package(args.output)
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

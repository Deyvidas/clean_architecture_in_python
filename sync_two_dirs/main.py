import hashlib
import os
from enum import Enum
from pathlib import Path
from typing import Required
from typing import TypedDict
from typing import Unpack


def hash_file(path: Path) -> str:
    hasher = hashlib.sha1()
    with path.open('rb') as file:
        hasher.update(file.read())
    return hasher.hexdigest()


def read_paths_and_hashes(path: Path) -> dict[str, Path]:
    hash_path = dict()
    for root, _, files in path.walk():
        for file in files:
            file_path = root / file
            hash_path[hash_file(file_path)] = file_path
    return hash_path


def copy(file: Path, to_dir: Path) -> str:
    command = f'cp {file} {to_dir}'
    while not (to_dir / file.name).exists():
        os.popen(command)
    return command


def delete(file: Path) -> str:
    command = f'rm {file}'
    while file.exists():
        os.popen(command)
    return command


def rename(old_path: Path, new_path: Path) -> str:
    command = f'mv {old_path} {new_path}'
    while not new_path.exists():
        os.popen(command)
    return command


class DetermineActionsKwargs(TypedDict):
    src_hashes: Required[dict[str, Path]]
    dst_hashes: Required[dict[str, Path]]
    src_root: Required[Path]
    dst_root: Required[Path]


def determine_actions(**kwargs: Unpack[DetermineActionsKwargs]):
    """Return actions that need to synchronize source with destination

    Args:
        hashes: The key is a hash of the file on the path saved in the value;
        root: The path of the root directory;

    Yields:
        tuple: Where the first is the name of an action, the remaining are arguments.
    """

    for src_hash, src_path in kwargs['src_hashes'].items():
        # If the file is not in the destination directory.
        if kwargs['dst_hashes'].get(src_hash, None) is None:
            yield ('COPY', src_path, kwargs['dst_root'])

        # If the file is in the destination directory but has a different name.
        elif (dp := kwargs['dst_hashes'][src_hash]).name != src_path.name:
            yield ('RENAME', dp, dp.parent / src_path.name)

    # If the file is in the destination directory but not in the source directory.
    extra_hashes = set(kwargs['dst_hashes']) - set(kwargs['src_hashes'])
    for hash in extra_hashes:
        yield ('DELETE', kwargs['dst_hashes'][hash])


class ActionsEnum(Enum):
    COPY = copy
    DELETE = delete
    RENAME = rename


def sync(src_root: Path, dst_root: Path):
    src_hashes = read_paths_and_hashes(src_root)
    dst_hashes = read_paths_and_hashes(dst_root)

    actions = determine_actions(
        src_hashes=src_hashes,
        dst_hashes=dst_hashes,
        src_root=src_root,
        dst_root=dst_root,
    )

    for action, *paths in actions:
        function = getattr(ActionsEnum, action)
        function(*paths)


def main():
    ...


if __name__ == '__main__':
    main()

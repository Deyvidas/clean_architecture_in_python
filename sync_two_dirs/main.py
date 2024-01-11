import hashlib
import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(kw_only=True)
class Result:
    copy_from_source: list[str]
    delete_from_dest: list[str]
    rename_in_dest: list[str]


def hash_file(path: Path) -> str:
    hasher = hashlib.sha1()
    with path.open('rb') as file:
        hasher.update(file.read())
    return hasher.hexdigest()


def get_hashes(path: Path) -> dict[str, Path]:
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
    while file.exists():
        os.remove(file)
    return f'rm {file}'


def rename(old_path: Path, new_path: Path) -> str:
    command = f'mv {old_path} {new_path}'
    while not new_path.exists():
        os.popen(command)
    return command


def sync(source: Path, dest: Path) -> Result:
    source_hashes = get_hashes(source)
    dest_hashes = get_hashes(dest)

    copy_from_source = set(source_hashes) - set(dest_hashes)
    delete_from_dest = set(dest_hashes) - set(source_hashes)
    rename_in_dest = set()

    for hash, path in dest_hashes.items():
        if hash in copy_from_source | delete_from_dest:
            continue
        if path.name == source_hashes[hash].name:
            continue
        rename_in_dest.add(hash)

    result = Result(
        copy_from_source=list(),
        delete_from_dest=list(),
        rename_in_dest=list(),
    )

    for c in copy_from_source:
        command = copy(source_hashes[c], dest)
        result.copy_from_source.append(command)
        print(command)

    for d in delete_from_dest:
        command = delete(dest_hashes[d])
        result.delete_from_dest.append(command)
        print(command)

    for r in rename_in_dest:
        old_path = dest_hashes[r]
        new_path = old_path.parent / source_hashes[r].name
        command = rename(old_path, new_path)
        print(command)

    return result


def main():
    ...


if __name__ == '__main__':
    main()

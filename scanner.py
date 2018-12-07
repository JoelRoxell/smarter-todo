from __future__ import annotations
from typing import Iterable, Tuple, NamedTuple, Optional, Dict, List
import os
import re
import functools

from functional.composition import compose

CORE_DIR = './sample'
pattern = re.compile(
    r'^(?:\s*(?://|\*))?\s*TODO:\s*(?P<description>.*?)\s*'
    r'(?:\[(?P<labels>[A-z0-9_\-\s,]+)]\s*)?'
    r'(?:(?P<estimate>[0-9]+[mh])\s*)?$')
filter_files = functools.partial(filter, lambda x: os.path.isfile(x))

Lines = Iterable[Tuple[str, int, str]]


class Issue(NamedTuple):
    file_path: str
    line: int
    description: str
    labels: List[Label]
    estimate: Optional[str]


class Label:
    __registry: Dict[str, Label] = {}

    def __new__(cls, name: str):
        if name in cls.__registry:
            return cls.__registry[name]
        return super(Label, cls).__new__(cls)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name


def get_files(directory: str) -> Iterable[str]:
    for dir_name, _, file_list in os.walk(directory):
        make_abs = functools.partial(
            map, lambda x: os.path.abspath(os.path.join(dir_name, x)))
        yield from filter_files(make_abs(file_list))


def get_lines(file_paths: Iterable[str]) -> Lines:
    for file_path in file_paths:
        with open(file_path, 'r') as f:
            for n, line in enumerate(f.readlines()):
                yield file_path, n, line.strip()


def get_labels(label_string: Optional[str]) -> Iterable[Label]:
    if not label_string:
        return
    for s in label_string.split(','):
        yield Label(s.strip())


def get_issues(lines: Lines) -> Iterable[Issue]:
    for path, n, line in lines:
        match = pattern.match(line)
        if not match: continue
        description, label_string, estimate = match.groups()
        labels = list(get_labels(label_string))
        yield Issue(path, n, description, labels, estimate)


scan = compose(get_issues, get_lines, get_files)

if __name__ == '__main__':
    import json
    for issue in scan(CORE_DIR):
        print(json.dumps(issue._asdict(), indent=4, default=lambda o: str(o)))

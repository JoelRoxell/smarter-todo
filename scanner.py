import os
import re


CORE_DIR = './sample'


class Issue():
    def __init__(self, description, labels, estimate):
        self.description = description
        self.labels = labels
        self.estimate = estimate


def extract_data_from_line(line):
    return\
        re.search(r'TODO:(.*?)\[', line),\
        re.search(r'\[(.*?)\]', line),\
        re.search(r'([0-9]+[m|h])', line)


def get_issues_from_file(file_path):
    with open(file_path) as file:
        for data in filter(
            lambda x: x[0] is not None,
            [extract_data_from_line(line) for line in file.read().split('\n')]
        ):
            yield Issue(
                str.strip(data[0].group(1)),
                data[1].group(1).split(','),
                data[2].group(1)
            )


def get_issues(directory, issues=[]):
    for dir_name, subs, file_list in os.walk(directory):
        for file_path in filter(lambda x: os.path.isfile(x), map(
            lambda x: os.path.abspath("{}/{}".format(dir_name, x)), file_list
        )):
            issues += get_issues_from_file(file_path)

    return issues


for issue in get_issues(CORE_DIR):
    print(issue.__dict__)

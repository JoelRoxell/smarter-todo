import os
import re
import string
import argparse
import multiprocessing


from github_integration import Github
from models.issue import Issue


def extract_data_from_line(line):
    # TODO: add regexe(s) for: assignees and body?
    # FIXME: .Comments may stretch multiple lines.
    return\
        re.search(r'TODO:(.*?)\[', line),\
        re.search(r'\[(.*?)\]', line),\
        re.search(r'([0-9]+[m|h])', line)


def get_issues_from_file(file_path):
    with open(file_path) as file:
        return [
            Issue(
                str.strip(data[0].group(1)),
                data[1].group(1).replace(' ', '').split(','),
                data[2].group(1)
            ) for data in filter(
                lambda x: x[0] is not None, [
                    extract_data_from_line(line)
                    for line in file.read().split('\n')
                ]
            )
        ]


def get_issues(directory, issues=[]):
    for dir_name, _, file_list in os.walk(directory):
        for file_path in filter(lambda x: os.path.isfile(x), map(
            lambda x: os.path.abspath("{}/{}".format(dir_name, x)), file_list
        )):
            issues += get_issues_from_file(file_path)

    return issues


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create issues from todo(s).')
    parser.add_argument(
        '--path',
        dest='project_path',
        type=str,
        help='Absolute path to the folder to be scanned'
    )
    parser.add_argument(
        '--owner',
        dest='owner',
        type=str,
        help='owner'
    )
    parser.add_argument(
        '--target',
        dest='target',
        type=str,
        help='target repo'
    )
    parser.add_argument(
        '--cpus',
        dest='CPUs',
        type=int,
        help='allowed threading capabilities',
        default=multiprocessing.cpu_count()
    )

    config = parser.parse_args()
    issues = get_issues(config.project_path)

    print(config)

    def create_issue(issue):
        print('Creating: {}'.format(issue.title))
        print(vars(issue))

        Github(config.owner, config.target).createIssue(
            issue.to_github_issue()
        )

    multiprocessing.Pool(processes=config.CPUs).map(create_issue, issues)

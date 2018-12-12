import re
import argparse
import multiprocessing

from tabulate import tabulate

from smartertodo.comments import get_comments_from_directory

from github_integration import Github
from models.issue import Issue


def extract_data_from_text(text):
    # TODO: add regexe(s) for: assignees and body?
    return\
        re.search(r'TODO:(.*?)\[', text),\
        re.search(r'\[(.*?)\]', text),\
        re.search(r'([0-9]+[m|h])', text)


def get_issues_from_comments(comments):
    return [
        Issue(
            str.strip(data[0].group(1)),
            data[1].group(1).replace(' ', '').split(',')
            if len(data) > 1 and data[1] else None,
            data[2].group(1)
            if len(data) > 2 and data[2] else None
        ) for data in filter(
            lambda x: len(x) > 0 and x[0] is not None, [
                extract_data_from_text(comment.value.replace('\n', ''))
                for comment in comments
            ]
        )
    ]


def get_issues(directory):
    return get_issues_from_comments(get_comments_from_directory(directory))


def run():
    parser = argparse.ArgumentParser(description='Create issues from todo(s).')
    parser.add_argument(
        '--path',
        dest='project_path',
        type=str,
        help='Absolute path to the folder to be scanned',
        required=True
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
    parser.add_argument(
        '--dry',
        type=bool,
        help='Only print issues'
    )

    config = parser.parse_args()

    issues = get_issues(config.project_path)

    if config.dry:
        print(tabulate([issue.__dict__ for issue in issues], headers='keys'))
    else:
        def create_issue(issue):
            print('Creating: {}'.format(issue.title))
            print(vars(issue))

            Github(config.owner, config.target).createIssue(
                issue.to_github_issue()
            )

        multiprocessing.Pool(processes=config.CPUs).map(create_issue, issues)

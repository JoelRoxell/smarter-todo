# smarter-todo

Create issues from TODO comments.

## Usage
> To use it with Github, set your token:
    export GITHUB_ACCESS_TOKEN=<token>

> Install it

    python setup.py install

> Now the command is available for you to run:

    smartertodo --path <path-to-project-files> --owner <owner> --target <repo> --dry <true|false>

> Example:

    smartertodo --path=sample --dry=true
    
    {'estimate': '2h', 'labels': ['discuss', 'test'], 'title': 'Should pass system configuration as a param. and this comment has multiple lines.'}
    {'estimate': '45m', 'labels': ['critical', 'test'], 'title': 'Should return a new issue'}
    {'estimate': '10m', 'labels': ['normal', 'frontend', 'test'], 'title': 'This is the sub.'}

## Running the tests
> To run the tests:

    pip install pytest
    py.test

## TODO:
1. resolve project path if passed param is relative.
2. __[FIXED]__ _cover comments where the TODO stretches more than 1 line._
3. find FIXME(s) and maybe other standards?
4. improve README
5. publish to pip or w/e

# smarter-todo

[![Build Status](https://travis-ci.com/JoelRoxell/smarter-todo.svg?branch=master)](https://travis-ci.com/JoelRoxell/smarter-todo)

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

    estimate    labels                          title
    ----------  ------------------------------  ---------------------------------------------------------------------------------
    2h          ['discuss', 'test']             Should pass system configuration as a param. and this comment has multiple lines.
    45m         ['critical', 'test']            Should return a new issue
    10m         ['normal', 'frontend', 'test']  This is the sub.

## Running the tests

> To run the tests:

    pip install pytest
    py.test

## TODO:

1. resolve project path if passed param is relative.
2. **[FIXED]** _cover comments where the TODO stretches more than 1 line._
3. find FIXME(s) and maybe other standards?
4. improve README
5. publish to pip or w/e

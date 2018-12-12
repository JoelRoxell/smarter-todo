from smartertodo.comments import get_comments_from_directory


def get_todos_from_directory(dirname):
    return filter(
        lambda x: 'TODO' in x.value,
        get_comments_from_directory(dirname)
    )

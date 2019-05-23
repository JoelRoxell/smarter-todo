from smartertodo.comments import get_comments_from_text


def test_get_comments_from_text():
    text = '''
    /* nice function */
    int somefunction() {
        return 1 + 1;
    };

    /*
    * This is a long
    * comment
    * with multiple
    * lines
    */
    int x = 2;

    # This is an inline comment
    # with multiple lines

    int y = 3; /* comment next to something */
    int xx = 3; # also comment next to something
    // this is another style of comment
    int p = y; // next
    '''

    comments = get_comments_from_text(text)
    assert len(comments) == 8

    assert comments[0].value == ' nice function '
    assert comments[1].value == '\n     This is a long\n     comment\n     with multiple\n     lines\n    '  # NOQA E501
    assert comments[2].value == ' This is an inline comment\n'
    assert comments[3].value == ' with multiple lines\n'
    assert comments[4].value == ' comment next to something '
    assert comments[5].value == ' also comment next to something\n'
    assert comments[6].value == ' this is another style of comment\n'
    assert comments[7].value == ' next\n'

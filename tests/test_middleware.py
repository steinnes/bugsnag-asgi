import traceback
import mock

from bugsnag_asgi import BugsnagMiddleware


def nester(total, exc_class=None):
    if exc_class is None:
        exc_class = Exception

    def inner(level):
        if level == 0:
            raise exc_class("I am an exception {} frames deep".format(total))
        return inner(level - 1)
    return inner(total)


def test_get_locals_returns_correct_frame_locals():
    mw = BugsnagMiddleware(mock.Mock())
    try:
        nester(3)
    except Exception as e:
        l = mw.get_locals(e)

    assert l['level'] == 0
    assert l['total'] == 3

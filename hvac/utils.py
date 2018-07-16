"""
Misc utility functions and constants
"""

import functools
import warnings
from textwrap import dedent

from hvac import exceptions


def raise_for_error(status_code, message=None, errors=None):
    """

    :param status_code:
    :type status_code:
    :param message:
    :type message:
    :param errors:
    :type errors:
    :return:
    :rtype:
    """
    if status_code == 400:
        raise exceptions.InvalidRequest(message, errors=errors)
    elif status_code == 401:
        raise exceptions.Unauthorized(message, errors=errors)
    elif status_code == 403:
        raise exceptions.Forbidden(message, errors=errors)
    elif status_code == 404:
        raise exceptions.InvalidPath(message, errors=errors)
    elif status_code == 429:
        raise exceptions.RateLimitExceeded(message, errors=errors)
    elif status_code == 500:
        raise exceptions.InternalServerError(message, errors=errors)
    elif status_code == 501:
        raise exceptions.VaultNotInitialized(message, errors=errors)
    elif status_code == 503:
        raise exceptions.VaultDown(message, errors=errors)
    else:
        raise exceptions.UnexpectedError(message)


def deprecated_method(to_be_removed_in_version, new_call_path=None, new_method=None):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used.

    :param to_be_removed_in_version: Version of this module the decorated method will be removed in.
    :type to_be_removed_in_version: str
    :param new_call_path: Example call to replace deprecated usage.
    :type new_call_path: str
    :param new_method: Method intended to replace the decorated method. This method's docstrings are included in the
        decorated method's docstring.
    :type new_method: function
    :return: Wrapped function that includes a deprecation warning and update docstrings from the replacement method.
    :rtype: types.FunctionType
    """
    def decorator(method):
        message = "Call to deprecated function '{old_func}'. This method will be removed in version '{version}'".format(
            old_func=method.__name__,
            version=to_be_removed_in_version,
        )
        if new_call_path:
            message += " Please use `{}` moving forward.".format(new_call_path)

        @functools.wraps(method)
        def new_func(*args, **kwargs):
            warnings.simplefilter('always', DeprecationWarning)  # turn off filter

            warnings.warn(
                message=message,
                category=DeprecationWarning,
                stacklevel=2,
            )
            warnings.simplefilter('default', DeprecationWarning)  # reset filter
            return method(*args, **kwargs)
        if new_method:
            new_func.__doc__ = dedent(
                """\
                {message}
                Docstring content from this method's replacement copied below:
                {new_docstring}
                """.format(
                    message=message,
                    new_docstring=new_method.__doc__,
                )
            )
        else:
            new_func.__doc__ = message
        return new_func
    return decorator

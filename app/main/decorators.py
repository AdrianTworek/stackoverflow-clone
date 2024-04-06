from django.contrib.auth.decorators import user_passes_test


def anonymous_required(function=None, redirect_url=None):
    """
    Decorator for views that checks that the user is not logged in, redirecting
    to the specified page if necessary.
    """
    if not redirect_url:
        redirect_url = '/'

    actual_decorator = user_passes_test(
        lambda u: u.is_anonymous,
        login_url=redirect_url
    )

    if function:
        return actual_decorator(function)
    else:
        return actual_decorator

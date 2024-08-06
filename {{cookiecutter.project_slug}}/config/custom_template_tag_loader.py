from importlib import import_module

from django.template.backends.django import get_package_libraries


def get_custom_template_tag_modules(candidates):
    """
    Yield custom template tag module names and their full import paths.

    :param candidates: A list of potential module paths to search for
    template tags.
    :return: A generator yielding tuples of (module_name, full_name).
    """
    for candidate in candidates:
        try:
            pkg = import_module(candidate)
        except ImportError:
            # No templatetags package defined. This is safe to ignore.
            continue

        if hasattr(pkg, "__path__"):
            for name in get_package_libraries(pkg):
                module_name = name[len(candidate) + 1 :]  # noqa: E203
                yield module_name, name


def get_custom_template_tags(folders):
    """
    Return a dictionary mapping custom template tag module names
    to their full import paths.

    :param folders: A list of folders to search for custom
     template tag modules.
    :return: A dictionary with module names as keys and full import paths
     as values.
    """
    return dict(get_custom_template_tag_modules(folders))

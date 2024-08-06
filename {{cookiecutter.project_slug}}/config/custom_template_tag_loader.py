from importlib import import_module

from django.template.backends.django import get_package_libraries


def get_custom_template_tag_modules(candidates):
    for candidate in candidates:
        try:
            pkg = import_module(candidate)
        except ImportError:
            # No templatetags package defined. This is safe to ignore.
            continue

        if hasattr(pkg, "__path__"):
            for name in get_package_libraries(pkg):
                yield name[len(candidate) + 1 :], name


def get_custom_template_tags(folders):
    return {
        module_name: full_name
        for module_name, full_name in get_custom_template_tag_modules(folders)
    }

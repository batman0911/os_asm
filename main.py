import isort
import sys
import platform
import importlib
from types import ModuleType


def get_stdlib_packages():
    if sys.version_info.minor == 10:
        module_names = sys.stdlib_module_names
    else:
        module_names = isort.stdlibs.py38.stdlib

    external_packages = set()
    for name in module_names:
        if name[0] == '_' or name == 'this' or name == 'antigravity':
            continue
        external_packages.add(name)
    return external_packages


def task1():
    external_packages = get_stdlib_packages()
    v = sys.version_info
    print(f'Python {v.major}.{v.minor}.{v.micro} on {platform.system()} {platform.release()}')
    print(f'Stdlib contains {len(external_packages)} external modules and packages: ')
    print(external_packages)


def get_real_packages(package_names):
    real_modules = set()
    not_importable_modules = set()
    for name in package_names:
        try:
            importlib.import_module(name)
            del sys.modules[name]
            real_modules.add(name)
        except:
            not_importable_modules.add(name)
    return real_modules, not_importable_modules


def get_real():
    external_packages = get_stdlib_packages()
    return get_real_packages(external_packages)


def task2():
    v = sys.version_info
    real_modules, not_importable_modules = get_real()
    print(f'These StdLib packages on Python-{v.major}.{v.minor}.{v.micro}/{platform.system()} {platform.release()} '
          f'are not importable:')
    print(not_importable_modules)


def module_dependency(module_names, name):
    dp_names = set()
    dp_dict = dict((md, 0) for md in module_names)
    for key, val in vars(sys.modules[name]).items():
        if isinstance(val, ModuleType):
            md_name = val.__name__

            try:
                index = md_name.index(".")
                md_name = md_name[0:index]
            except:
                pass

            dp_names.add(md_name)
            dp_dict[md_name] = dp_dict[md_name] + 1
            print(f'key: {key}, type: {type(val)}, val: {md_name}, module: {md_name}')

    return dp_names


def task3():
    real_modules = get_real()
    module_dependency(real_modules, 'locale')


if __name__ == '__main__':
    # task1()
    # task2()
    task3()

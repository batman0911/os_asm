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
            # del sys.modules[name]
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

    for name in real_modules:
        del sys.modules[name]


def module_dependency(module_names, name):
    if name not in module_names:
        raise Exception(f'{name} is not importable module')
    dp_names = set()

    try:
        importlib.import_module(name)
    except:
        print(f'err name: {name}')
    for key, val in vars(sys.modules[name]).items():
        if isinstance(val, ModuleType):
            md_name = val.__name__

            try:
                index = md_name.index(".")
                md_name = md_name[0:index]
            except:
                pass

            dp_names.add(md_name)
            # print(f'key: {key}, type: {type(val)}, val: {md_name}, module: {md_name}')

    # del sys.modules[name]

    return dp_names


def core_modules(real_modules):
    # real_modules, _ = get_real()
    core_module_names = set()
    for r_name in real_modules:
        dp_names = module_dependency(real_modules, r_name)
        if len(dp_names) == 0:
            core_module_names.add(r_name)

    return core_module_names


def most_dependent_modules(real_modules):
    dp_dict = dict((name, 0) for name in real_modules)
    for md_name in real_modules:
        count = len(module_dependency(real_modules, md_name))
        dp_dict[md_name] = count

    sorted_dp_dict = dict(sorted(dp_dict.items(), key=lambda item: item[1], reverse=True))
    i = 0
    most_dependent_module_names = dict()
    for k, v in sorted_dp_dict.items():
        if i > 5:
            break
        most_dependent_module_names[k] = v
        i = i + 1

    return most_dependent_module_names


def task3():
    real_modules, not_importable_modules = get_real()
    # print(f'real modules: {real_modules}')
    core_module_names = core_modules(real_modules)

    dp_dict = most_dependent_modules(real_modules)

    print(f'The following StdLib packages are most dependent:')
    for k, v in dp_dict.items():
        print(f'{k}: {v}')
    print(f'The {len(core_module_names)} core packages are:')
    print(core_module_names)

    for name in real_modules:
        del sys.modules[name]


if __name__ == '__main__':
    print(f'task1 -----------------')
    task1()

    print(f'task2 -----------------')
    task2()

    print(f'task3 -----------------')
    task3()

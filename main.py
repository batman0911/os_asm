import enum

import isort
import sys
import platform
import importlib
from types import ModuleType
import inspect


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

    # for name in real_modules:
    #     del sys.modules[name]


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

    return dp_names


def core_modules(real_modules):
    core_module_names = set()
    for r_name in real_modules:
        dp_names = module_dependency(real_modules, r_name)
        if len(dp_names) == 0:
            core_module_names.add(r_name)

    return core_module_names


def get_custom_sorted_dict_by_value(m_dict, num, is_reverse):
    sorted_dict = dict(sorted(m_dict.items(), key=lambda item: item[1], reverse=is_reverse))
    i = 0
    rd = dict()
    for k, v in sorted_dict.items():
        if i > num:
            break
        rd[k] = v
        i = i + 1
    return rd


def most_dependent_modules(real_modules):
    dp_dict = dict((name, 0) for name in real_modules)
    for md_name in real_modules:
        count = len(module_dependency(real_modules, md_name))
        dp_dict[md_name] = count

    return get_custom_sorted_dict_by_value(dp_dict, 5, True)


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

    # for name in real_modules:
    #     del sys.modules[name]


def module_class_count(module_names):
    md_class_count = dict()
    for md in module_names:
        count = 0
        for name, obj in inspect.getmembers(sys.modules[md]):
            if inspect.isclass(obj):
                if issubclass(obj, enum.Enum):
                    continue
                else:
                    count = count + 1
        md_class_count[md] = count
    return md_class_count


def largest_module_by_class(md_class_count):
    return get_custom_sorted_dict_by_value(md_class_count, 5, True)


def no_class_modules(md_class_count):
    no_cls_set = set()
    for k, v in md_class_count.items():
        if v == 0:
            no_cls_set.add(k)
    return no_cls_set


def explore_package(package_name):
    importlib.import_module(package_name)
    pack = sys.modules[package_name]
    file_name = 'builtin_binary'
    try:
        file_name = pack.__file__
        n = len(file_name)
        if file_name[n - 3:n] == '.py':
            return package_name, file_name, 0
        elif file_name[n - 3:n] == '.so':
            return package_name, file_name, 1
        else:
            raise Exception(f'unsupported file: {file_name}')
    except:
        return package_name, file_name, 2


def get_py_modules(module_names):
    py_mds = set()
    for md in module_names:
        p, f, t = explore_package(md)
        if t == 0:
            py_mds.add((p, f))
    return py_mds


def count_file_line(file_path):
    count = 0
    for line in open(file_path, encoding="utf8"):
        count += 1
    return count


def get_file_lines_dict(module_names):
    md_lines = dict()
    py_mds = get_py_modules(module_names)
    for py_md in py_mds:
        key = py_md[0]
        num_lines = count_file_line(py_md[1])
        md_lines[key] = num_lines
    return md_lines


def largest_module_by_line(md_lines):
    return get_custom_sorted_dict_by_value(md_lines, 5, True)


def smallest_module_by_line(md_lines):
    return get_custom_sorted_dict_by_value(md_lines, 5, False)


def task4():
    real_modules, _ = get_real()
    md_class_count = module_class_count(real_modules)
    lg_md_cl = largest_module_by_class(md_class_count)
    n_cl_md = no_class_modules(md_class_count)

    md_lines = get_file_lines_dict(real_modules)
    lg_md_line = largest_module_by_line(md_lines)
    sml_md_line = smallest_module_by_line(md_lines)

    print(f'largest modules by class: ')
    print(lg_md_cl)

    print(f'modules with no class: ')
    print(n_cl_md)

    print(f'largest modules by line: ')
    print(lg_md_line)

    print(f'smallest modules by line: ')
    print(sml_md_line)


if __name__ == '__main__':
    # print(f'task1 -----------------')
    # task1()
    #
    # print(f'task2 -----------------')
    # task2()
    #
    # print(f'task3 -----------------')
    # task3()

    print(f'task4 -----------------')
    task4()

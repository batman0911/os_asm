import isort
import sys
import platform


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


if __name__ == '__main__':
    # externel_packages = get_stdlib_packages()
    # print(externel_packages)
    task1()
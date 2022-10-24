"""
Template for the COMP1730/6730 project assignment, S2 2022.
The assignment specification is available on the course web
site, at https://cs.anu.edu.au/courses/comp1730/assessment/project/

Collaborators: <list the UIDs of ALL members of your project group here>
"""

import ast
import imp
import importlib
import os
import platform
import sys
from types import ModuleType

import isort
import matplotlib.pyplot as plt
import networkx as nx


def get_stdlib_packages():
    if sys.version_info.minor == 10:
        module_names = sys.stdlib_module_names
    else:
        module_names = isort.stdlibs.py38.stdlib

    external_packages = list()
    for name in module_names:
        if name[0] == '_' or name == 'this' or name == 'antigravity':
            continue
        external_packages.append(name)
    return external_packages


def get_version():
    v = sys.version_info

    return str(v.major) + str(v.minor) + str(v.micro)


def task1():
    external_packages = get_stdlib_packages()
    v = sys.version_info
    print(f'Python {v.major}.{v.minor}.{v.micro} on {platform.system()} {platform.release()}')
    print(f'Stdlib contains {len(external_packages)} external modules and packages: ')
    print(external_packages)


def get_real_packages(package_names):
    """Loop through modules and try to import a single module
        return list of real modules (importable) and list of 'not importable' modules
    """

    real_modules = list()
    not_importable_modules = list()
    for name in package_names:
        try:
            importlib.import_module(name)
            real_modules.append(name)
        except:
            not_importable_modules.append(name)
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
    """Get the list of dependencies of a module 'name',
        check if that module is in real module list"""

    if name not in module_names:
        raise Exception(f'{name} is not importable module')
    dp_names = list()
    for key, val in vars(sys.modules[name]).items():
        if isinstance(val, ModuleType):
            md_name = val.__name__

            try:
                index = md_name.index(".")
                md_name = md_name[0:index]
            except:
                pass

            if md_name != name:
                dp_names.append(md_name)

    return dp_names


def core_modules(real_modules):
    # Get list of modules with no dependencies
    core_module_names = list()
    for r_name in real_modules:
        dp_names = module_dependency(real_modules, r_name)
        if len(dp_names) == 0:
            core_module_names.append(r_name)

    return core_module_names


def get_custom_sorted_dict_by_value(m_dict, num, it_idx, is_reverse):
    """Sort the dictionary by its value
        num: number of first elements to return
        it_idx: index of value item if value is a tuple
        is_reverse: reversed order or not"""

    if it_idx is not None:
        sorted_dict = dict(sorted(m_dict.items(), key=lambda item: item[1][it_idx], reverse=is_reverse))
    else:
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
    """Get 5 most dependent modules"""

    dp_dict = dict((name, 0) for name in real_modules)
    for md_name in real_modules:
        count = len(module_dependency(real_modules, md_name))
        dp_dict[md_name] = count

    return get_custom_sorted_dict_by_value(dp_dict, 5, None, True)


def task3():
    real_modules, not_importable_modules = get_real()
    core_module_names = core_modules(real_modules)

    dp_dict = most_dependent_modules(real_modules)

    print(f'The following StdLib packages are most dependent:')
    for k, v in dp_dict.items():
        print(f'{k}: {v}')
    print(f'The {len(core_module_names)} core packages are:')
    print(core_module_names)


def get_package_info(package_name):
    """Return package name, file name and type of package
        0: python file
        otherwise: not python file"""

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


def count_file_line(file_path):
    """Count number of lines of a file by opening it"""

    count = 0
    for line in open(file_path, encoding="utf8"):
        count += 1
    return count


def count_file_class(filename):
    """Count number of custom classes of a python file"""

    with open(filename, encoding='utf8') as file:
        name = os.path.basename(filename)
        if name == 'py2_test_grammar.py':
            return 12
        try:
            node = ast.parse(file.read())
            classes = [n for n in node.body if isinstance(n, ast.ClassDef)]
            return len(classes)
        except:
            print(f'err in file: {filename}')
            return 0


def list_file_in_module(module_name):
    """List all python files in a module
        ignore __pycache__ folder"""

    MODULE_EXTENSIONS = ('.py')
    file, pathname, description = imp.find_module(module_name)

    if os.path.isdir(pathname):
        file_list = list()
        for (root, dirs, files) in os.walk(pathname, topdown=True):
            if os.path.basename(root) == '__pycache__':
                continue
            if len(files) > 0:
                for filename in files:
                    if filename.endswith(MODULE_EXTENSIONS):
                        file_list.append(os.path.join(root, filename))

        return pathname, 'dir', file_list


    else:
        return pathname, 'file', [pathname]


def explore_package(name):
    """Explore a package by name
        return number of lines, number of classes (all files if module is a directory)
            and type of module (False for binary and True for python module)"""

    md_name, md_file, md_type = get_package_info(name)

    if md_type != 0:
        return 0, 0, False

    module_dir, module_type, file_list = list_file_in_module(name)
    if module_type == 'file':
        file_lines = count_file_line(module_dir)
        file_classes = count_file_class(module_dir)
        return file_lines, file_classes, True

    else:
        count_lines = 0
        count_classes = 0
        for file_name in file_list:
            count_lines = count_lines + count_file_line(file_name)
            count_classes = count_classes + count_file_class(file_name)
        return count_lines, count_classes, True


def build_module_info_dict(module_names):
    """Building a dictionary with module name is the key and 'explore_package' is the value"""
    
    md_dict = dict()
    for md in module_names:
        md_dict[md] = explore_package(md)

    return md_dict


def modules_info_python_only(md_dict):
    """Dictionary of module info for python modules only"""
    
    pmd = dict()
    for k, v in md_dict.items():
        if v[2]:
            pmd[k] = (v[0], v[1])
    return pmd


def largest_module_by_class(md_dict):
    return get_custom_sorted_dict_by_value(md_dict, 5, 1, True)


def no_class_modules(md_dict):
    no_cls_set = list()
    for k, v in md_dict.items():
        if v[1] == 0:
            no_cls_set.append(k)
    return no_cls_set


def largest_module_by_line(md_dict):
    return get_custom_sorted_dict_by_value(md_dict, 5, 0, True)


def smallest_module_by_line(md_lines):
    return get_custom_sorted_dict_by_value(md_lines, 5, 0, False)


def task4():
    real_modules, _ = get_real()
    md_info_dict = build_module_info_dict(real_modules)
    py_md_info_dict = modules_info_python_only(md_info_dict)

    lg_md_li = largest_module_by_line(py_md_info_dict)
    sml_md_li = smallest_module_by_line(py_md_info_dict)

    lg_md_cls = largest_module_by_class(py_md_info_dict)
    n_md_cls = no_class_modules(py_md_info_dict)

    print(f'5 largest module by line: ')
    for k, v in lg_md_li.items():
        print(f'{k}: {v[0]}')

    print(f'\n5 smallest module by line: ')
    for k, v in sml_md_li.items():
        print(f'{k}: {v[0]}')

    print(f'\n5 largest module by class: ')
    for k, v in lg_md_cls.items():
        print(f'{k}: {v[1]}')

    print(f'\nmodules with no custom classes: ')
    print(n_md_cls)


def module_dependency_map(modules):
    """Building a dictionary of module dependencies
        key: module name
        value: its dependencies"""
    
    md_map = dict()
    for md in modules:
        md_map[md] = module_dependency(modules, md)
    return md_map


def build_adj_edge_graph(md_map):
    """Convert dependency dictionary to map of number
        building adjacency list of edges
        packages as nodes and their dependencies as links between the nodes"""
    
    index_list = list()

    for k, v in md_map.items():
        index_list.append(k)

    n = len(index_list)
    adj_list = list()
    for i in range(n):
        adj_list.append([])

    for md in index_list:
        for name in md_map[md]:
            try:
                i = index_list.index(md)
                j = index_list.index(name)
                if j not in adj_list[i]:
                    adj_list[i].append(j)
            except:
                continue

    return adj_list, index_list


def print_cycle(stack, v, circle_list):
    """print the cycle in graph"""
    
    st2 = [stack.pop()]
    while st2[-1] != v:
        st2.append(stack.pop())

    rs = []
    while len(st2) > 0:
        rs.append(st2[-1])
        stack.append(st2[-1])
        st2.pop()

    circle_list.append(rs)


def process_DFS_tree(graph, stack, visited_vertices, circle_list):
    """Build depth first search tree"""
    
    for v in graph[stack[-1]]:
        if visited_vertices[v] == 'in_stack':
            print_cycle(stack, v, circle_list)
        elif visited_vertices[v] == 'not_visited':
            stack.append(v)
            visited_vertices[v] = 'in_stack'
            process_DFS_tree(graph, stack, visited_vertices, circle_list)

    visited_vertices[stack[-1]] = 'done'
    stack.pop()


def find_cycles(graph, circle_list):
    """Find all cycles in a graph"""
    
    n = len(graph)
    visited = list()
    for i in range(n):
        visited.append('not_visited')

    for v in range(n):
        if visited[v] == 'not_visited':
            stack = [v]
            visited[v] = 'in_stack'
            process_DFS_tree(graph, stack, visited, circle_list)


def task5():
    real_modules, _ = get_real()
    md_map = module_dependency_map(real_modules)
    adj_list, index_list = build_adj_edge_graph(md_map)
    circle_list = []
    find_cycles(adj_list, circle_list)

    print(f'The StdLib packages form a cycle of dependency: ')
    i = 1
    for item in circle_list:
        rs = f'{i}. '
        for v in item:
            rs = rs + index_list[v] + ' -> '
        print(rs[0:(len(rs) - 4)])


def build_adj_list_md(md_map):
    edges = list()

    for k, v in md_map.items():
        for name in v:
            edges.append(tuple([k, name]))

    return edges


def define_graph(md_map):
    edges = build_adj_list_md(md_map)
    return nx.DiGraph(edges)


def plot(DG):
    plt.figure(3, figsize=(60, 60))
    nx.draw_spring(DG, edge_color="r", font_size=10, with_labels=True)
    ax = plt.gca()
    ax.margins(0.08)
    plt.title(f'Module dependency graph of StdLib on python {get_version()}', fontsize=50)
    plt.show()


def task6():
    real_modules, _ = get_real()
    md_map = module_dependency_map(real_modules)
    DG = define_graph(md_map)
    plot(DG)


def remove_modules():
    module_names, _ = get_real()
    for name in module_names:
        del sys.modules[name]


def analyse_stdlib():
    print(f'task1 -----------------')
    task1()

    print(f'\ntask2 -----------------')
    task2()

    print(f'\ntask3 -----------------')
    task3()

    print(f'\ntask4 -----------------')
    task4()

    print(f'\ntask5 -----------------')
    task5()

    remove_modules()


# The section below will be executed when you run this file.
# Use it to run tests of your analysis function on the data
# files provided.

if __name__ == '__main__':
    NAME = 'John Smith'
    ID = 'u1234567'
    print(f'My name is {NAME}, my id is {ID}, and these are my findings for Project COMP1730.2022.S2')
    analyse_stdlib()

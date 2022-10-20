import sys
from types import ModuleType

if __name__ == '__main__':
    print(vars(sys.modules['cmath']))
    # for key, val in vars(sys.modules['cmath']).items():
    #     if isinstance(val, ModuleType):
    #         md_name = val
    #
    #         try:
    #             index = md_name.index(".")
    #             md_name = md_name[0:index]
    #         except:
    #             pass
    #
    #         print(f'key: {key}, type: {type(val)}, val: {md_name}, module: {md_name}')
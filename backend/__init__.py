import os
import sys

project_dir = os.path.abspath(os.path.dirname("."))
sys.path.append(project_dir)

root_dir = "Some random String"

if __name__ == '__main__':
    print(project_dir)


#!/usr/bin/env python
import sys
import importlib


def main(repo_path, app_name):
    sys.path.append(repo_path)
    app = importlib.import_module(app_name)
    sys.stdout.write(app.__version__)


if __name__ == '__main__':
    repo_path = sys.argv[1]
    app_name = sys.argv[2]
    main(repo_path, app_name)

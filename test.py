#!/usr/bin/env python

import json
import pathlib


CONFIG_PATH = pathlib.Path.home() / '.config/dotman/config.json'
if CONFIG_PATH.exists():
    with open(pathlib.Path.home() / '.config/dotman/config.json') as config:
        CONFIG = config.read()
    CONFIG = json.loads(CONFIG)

# print(str(CONFIG['dirs_to_copy']))
# print(str(CONFIG['files_to_copy']))
FILES_TO_COPY = []
for path in CONFIG['files_to_copy']:
    for path, files in path.items():
        for file in files:
            FILES_TO_COPY.append(path + "/" + file)
print(str(FILES_TO_COPY))

DIRS_TO_COPY = []
for path in CONFIG['dirs_to_copy']:
    for path, dirs in path.items():
        for dir_ in dirs:
            DIRS_TO_COPY.append(path + "/" + dir_)


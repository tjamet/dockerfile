import re
import tempfile
import json
from shutil import move
from os import fdopen, remove


def write_json_to_temp_file(data):
    """Writes JSON data to a temporary file and returns the path to it"""
    fp = tempfile.NamedTemporaryFile(delete=False)
    fp.write(json.dumps(data).encode('utf-8'))
    fp.close()
    return fp.name


def replace_in_file(file_path, pattern, subst):
    fh, abs_path = tempfile.mkstemp()
    with fdopen(fh, 'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                new_file.write(re.sub(pattern, subst, line, 0, re.IGNORECASE))

    remove(file_path)
    move(abs_path, file_path)

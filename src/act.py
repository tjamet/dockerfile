import json
from subprocess import run

from utils import write_json_to_temp_file, replace_in_file


def act():
    with open('/dependencies/input_data.json', 'r') as f:
        data = json.load(f)

    run(['deps', 'branch'], check=True)

    for manifest_path, manifest_data in data.get('manifests', {}).items():
        for dependency_name, updated_dependency_data in manifest_data['updated']['dependencies'].items():
            installed = manifest_data['current']['dependencies'][dependency_name]['constraint']
            version_to_update_to = updated_dependency_data['constraint']

            if installed == 'latest':
                # may or not actually have :latest in the line
                pattern = r'(FROM\s+{})(?::latest)?(\s+.*)'.format(dependency_name)
            else:
                pattern = r'(FROM\s+{}):{}(\s+.*)'.format(dependency_name, installed)

            replace_in_file(manifest_path, pattern, r'\1:{}\2'.format(version_to_update_to))

            run(['deps', 'commit', '-m', 'Update {} from {} to {}'.format(dependency_name, installed, version_to_update_to), manifest_path], check=True)

    run(['deps', 'pullrequest', write_json_to_temp_file(data)], check=True)

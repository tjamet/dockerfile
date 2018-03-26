import re
import sys
from subprocess import run

import requests

from utils import write_json_to_temp_file


def collect():
    dockerfile_path = sys.argv[1]

    collected_dependencies = {}

    with open(dockerfile_path, 'r') as f:
        stages = []

        for line in f.readlines():

            built_state_match_re = re.match('(FROM\s+.*)AS\s+([^\s]+)\s*$', line, re.IGNORECASE)
            if built_state_match_re:
                line = built_state_match_re.groups()[0]
                stages.append(built_state_match_re.groups()[1])

            owner_repo_tag_match = re.match('FROM\s+([^\/\s:]*)/([^\/\s:]*):([^\/\s:]*)$', line, re.IGNORECASE)
            if owner_repo_tag_match:
                owner = owner_repo_tag_match.groups()[0]
                repo = owner_repo_tag_match.groups()[1]
                tag = owner_repo_tag_match.groups()[2]

                collected_dependencies[f'{owner}/{repo}'] = {
                    'constraint': tag,
                }
                continue

            owner_repo_match = re.match('FROM\s+([^\/\s:]*)/([^\/\s:]*)$', line, re.IGNORECASE)
            if owner_repo_match:
                owner = owner_repo_match.groups()[0]
                repo = owner_repo_match.groups()[1]

                collected_dependencies[f'{owner}/{repo}'] = {
                    'constraint': 'latest',
                }
                continue

            repo_tag_match = re.match('FROM\s+([^\/\s:]*):([^\/\s:]*)$', line, re.IGNORECASE)
            if repo_tag_match:
                repo = repo_tag_match.groups()[0]
                tag = repo_tag_match.groups()[1]

                collected_dependencies[repo] = {
                    'constraint': tag,
                }
                continue

            repo_match = re.match('FROM\s+([^\/\s:]*)$', line, re.IGNORECASE)
            if repo_match:
                repo = repo_match.groups()[0]

                if repo in stages:
                    # if this is a stage built before
                    continue

                collected_dependencies[repo] = {
                    'constraint': 'latest',
                }
                continue

    for name, data in collected_dependencies.items():
        data['source'] = 'dockerhub'

        response = requests.get(f'https://registry.hub.docker.com/v1/repositories/{name}/tags')
        response.raise_for_status()

        # is there any way to filter out the versios below the constraint?
        # could just slice off the list, but that might not work... looks like "latest" then alphabetical
        data['available'] = [{'name': x['name']} for x in response.json()]

    manifest_output = {
        "manifests": {
            dockerfile_path: {
                "current": {
                    "dependencies": collected_dependencies
                }
            }
        }
    }

    run(['deps', 'collect', write_json_to_temp_file(manifest_output)], check=True)

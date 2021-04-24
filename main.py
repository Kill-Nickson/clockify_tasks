import os
import json

import requests
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv('API_KEY')
API_BASE_ENDPOINT = 'https://api.clockify.me/api/v1'
headers = {'x-api-key': API_KEY}


def get_workspaces():
    endpoint = API_BASE_ENDPOINT + '/workspaces'
    response = requests.get(endpoint, headers=headers)
    workspaces = json.loads(response.content)
    return workspaces


def get_workspace_id_by_name(workspaces, name):
    for w in workspaces:
        if w['name'] == name:
            return w['id']


def get_projects_by_workspace_id(ws_id):
    endpoint = API_BASE_ENDPOINT + f'/workspaces/{ws_id}/projects'
    response = requests.get(endpoint, headers=headers)
    projects = json.loads(response.content)
    return projects


def get_project_tasks(ws_id, project_id):
    endpoint = API_BASE_ENDPOINT + f'/workspaces/{ws_id}/projects/{project_id}/tasks'
    response = requests.get(endpoint, headers=headers)
    tasks = json.loads(response.content)
    return tasks


def get_all_tasks():
    workspaces = get_workspaces()
    workspaces_with_projects = {w['name']: get_projects_by_workspace_id(w['id']) for w in workspaces}
    for w_name, w_projects in workspaces_with_projects.items():
        print(w_name)
        for project in w_projects:
            print('\t', project['name'])

            tasks = get_project_tasks(get_workspace_id_by_name(workspaces, w_name), project['id'])
            # Tasks grouped by adding time
            tasks = tasks[::-1]
            for n, t in enumerate(tasks):
                print('\t\t', n+1, t['name'], '(time spent:', t['duration'][2:], ')')


if __name__ == '__main__':
    get_all_records()

import json
import os
import requests
import sys
import yaml


def get_session():
    """
    get token by POST request
    :return: token
    """
    url = 'https://build.osinfra.cn/api/v1/session'
    username = os.getenv("ARGOCD_USERNAME")
    password = os.getenv("ARGOCD_PASSWORD")
    data = {
        "password": password,
        "username": username
    }
    r = requests.post(url, json.dumps(data))
    if r.status_code == 200:
        token = r.json()['token']
        return token


def get_cluster_names():
    """
    get cluster names by GET request
    :return: a list of cluster_names
    """
    token = get_session()
    headers = {
        'Cookie': 'argocd.token={}'.format(token)
    }
    r = requests.get('https://build.osinfra.cn/api/v1/clusters', headers=headers)  # status code 403,条件不足限制访问
    if r.status_code != 200:
        print('GET request failed')
        print(r.status_code, r.json())
        sys.exit(1)
    cluster_names = []
    for i in r.json()['items']:
        cluster_names.append(i['name'])
    return cluster_names


def get_files(root_path, yaml_files=[]):
    """
    find all yaml files under the dir tree
    :param root_path: the path start to search
    :param yaml_files: a list to store yaml files
    :return: yaml_files
    """
    files = os.listdir(root_path)
    for file in files:
        if not os.path.isdir(root_path + '/' + file):
            if file[-5:] == '.yaml':
                yaml_files.append(root_path + '/' + file)
        else:
            get_files((root_path + '/' + file), yaml_files)
    return yaml_files


def check_project_yaml(file_path, cluster_names):
    """
    check the file named project.yaml whether match the fits
    :param file_path: the path of a yaml file
    :param cluster_names: cluster_names
    :return: errors
    """
    errors = 0
    with open(file_path, 'r') as fp:
        content = yaml.load(fp.read(), Loader=yaml.FullLoader)
        name_list = []
        for i in content['spec']['destinations']:
            server = i['server'] if 'server' in i else ''
            name = i['name'] if 'name' in i else ''
            if server:
                print('Warning! server still remains in {}!'.format(file_path))
                errors += 1
            if name:
                name_list.append(name)
        if name_list:
            for name in name_list:
                if name not in cluster_names:
                    print('{} found in {} not in cluster names'.format(name, file_path))
                    errors += 1
        else:
            print('There is no name still in {}'.format(file_path))
            errors += 1
    return errors


def check_non_project_yaml(file_path, cluster_names):
    """
    check the file not named project.yaml whether match the fits
    :param file_path: the path of a yaml file
    :param cluster_names: cluster_names
    :return: errors
    """
    errors = 0
    with open(file_path, 'r') as fp:
        content = yaml.load(fp.read(), Loader=yaml.FullLoader)
        server = content['spec']['destination']['server'] if 'server' in content['spec']['destination'] else ''
        name = content['spec']['destination']['name'] if 'name' in content['spec']['destination'] else ''
        if server:
            print('Warning! server still remains in {}!'.format(file_path))
            errors += 1
        if not name:
            print('There is no name still in {}'.format(file_path))
            errors += 1
        elif name not in cluster_names:
            print('{} found in {} not in cluster names'.format(name, file_path))
            errors += 1
    return errors


if __name__ == '__main__':
    # 1.调用接口查询clusters的所有name
    cluster_names = get_cluster_names()

    # 2.查找给定目录下的所有yaml文件并保存
    yaml_files = get_files('./community')
    yaml_files_2 = get_files('./infra-common')
    yaml_files.extend(yaml_files_2)

    # 3.遍历cluster_names.txt,对project.yaml和非project.yaml作内容检查
    number = 0
    for yaml_file in yaml_files:
        if yaml_file.split('/')[-1] == 'project.yaml':
            errors = check_project_yaml(yaml_file, cluster_names)
            number += errors
        else:
            errors = check_non_project_yaml(yaml_file, cluster_names)
            number += errors
    if number != 0:
        print('FAILED :(')
    else:
        print('PASS :)')

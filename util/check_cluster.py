import glob
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
    username = os.getenv('ARGOCD_USERNAME', '')
    password = os.getenv('ARGOCD_PASSWORD', '')
    if not username or not password:
        print('Both username and password are required to get token.')
        print('Missing username or password,exit...')
        sys.exit(1)
    data = {
        "username": username,
        "password": password
    }
    r = requests.post(url, json.dumps(data))
    if r.status_code == 200:
        token = r.json()['token']
        return token
    else:
        print('Cannot get token!')
        print('status code: {}'.format(r.status_code))
        print(r.json())
        sys.exit(1)


def get_cluster_names():
    """
    get cluster names by GET request
    :return: a list of cluster_names
    """
    token = get_session()
    headers = {
        'Cookie': 'argocd.token={}'.format(token)
    }
    r = requests.get('https://build.osinfra.cn/api/v1/clusters', headers=headers)
    if r.status_code != 200:
        print('Cannot get cluster names because GET request failed.')
        print(r.status_code, r.json())
        sys.exit(1)
    cluster_names = []
    for i in r.json()['items']:
        cluster_names.append(i['name'])
    return cluster_names


def get_files():
    """
    return a list of yaml files
    :return: files
    """
    script_dir = os.path.split(os.path.realpath(__file__))[0]
    files = glob.glob(os.path.abspath(os.path.dirname(script_dir) + '/communities' + '/**/*.yaml'), recursive=True)
    files2 = glob.glob(os.path.abspath(os.path.dirname(script_dir) + '/infra-common' + '/**/*.yaml'), recursive=True)
    files.extend(files2)
    return files


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
            if server or not name:
                print('[Project Error] {0}: Please use name instead of server to configure the destination clusters, found {1} {2} !'.format(file_path, server, name))
                errors += 1
            if name:
                name_list.append(name)
        if name_list:
            for name in name_list:
                if name not in cluster_names:
                    print('[Project Error] {0}: Cluster Name {1} not found in our cluster names'.format(file_path, name))
                    errors += 1
    return errors


def check_application_yaml(file_path, cluster_names):
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
        if server or not name:
            print("[Application Error] {0}: Please use name instead of server to configure the destination cluster, found {1} {2}!".format(file_path, server, name))
            errors += 1
        elif name not in cluster_names:
            print('[Application Error] {0}: Cluster Name {1} not found in our cluster names'.format(file_path, name))
            errors += 1
    return errors


if __name__ == '__main__':
    # 1.调用接口查询clusters的所有name
    cluster_names = get_cluster_names()

    # 2.查找给定目录下的所有yaml文件
    yaml_files = get_files()

    # 3.分类对yaml作内容检查
    for yaml_file in yaml_files:
        if yaml_file.split('/')[-1] == 'project.yaml':
            check_project_yaml(yaml_file, cluster_names)
        else:
            check_application_yaml(yaml_file, cluster_names)
    sys.exit(-1)

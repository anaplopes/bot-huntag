import json
import requests


# Configurações da sua aplicação
client_id = 'bbc2dd9e-1d89-4468-86e5-52b0ee42306f'
tenant_id = 'f8cdef31-a31e-4b4a-93e4-5f571e91255a'
client_secret = 'TCA8Q~Pg8_7WRXP5CBFlRSl35gg1Pb2pRzaDMbfE'


def login():
    # url = 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize'
    url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'https://graph.microsoft.com/.default',
        'grant_type': 'client_credentials'
    }

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        access_token = json.loads(response.text)['access_token']
        return access_token

    return "Falha ao obter o token de acesso."


def upload_file(access_token: str, content_type: str, folder: str, file_name: str, file_path: str):
    ''' https://learn.microsoft.com/en-us/graph/api/driveitem-put-content?view=graph-rest-1.0&tabs=http
        [upload a new file] PUT /drives/{drive-id}/items/{parent-id}:/{filename}:/content
        [updating an existing file] PUT /drives/{drive-id}/items/{item-id}/content
    '''

    url = f'https://graph.microsoft.com/v1.0/drive/root:/{folder}/{file_name}:/content'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': content_type
    }

    with open(f'{file_path}/{file_name}', 'rb') as file:
        file_content = file.read()

    response = requests.put(url, headers=headers, data=file_content)
    if response.status_code == 200 or response.status_code == 201:
        return {
            "status_code": response.status_code,
            "message": "Arquivo enviado com sucesso."
        }

    return {
        "status_code": response.status_code,
        "message": json.loads(response.text)
    }

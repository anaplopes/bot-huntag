import json
import requests
from src.settings import settings


class APIGraph:

    def login():
        tenant_id = settings.AZURE_DIRETORY_TENANT_ID
        url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'client_id': settings.AZURE_APP_CLIENT_ID,
            'client_secret': settings.AZURE_APP_CLIENT_SECRET,
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

        with open(f'{settings.PATH_DIR_SOURCE}/{file_name}', 'rb') as file:
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

import requests

with open('YA_TOKEN.txt', encoding='utf-8') as file:
    YA_TOKEN = file.read()


class YaUploader:
    main_url = 'https://cloud-api.yandex.net/v1/disk/'
    main_headers = {
        'Authorization': YA_TOKEN
    }

    def create_folder(self, folder_name: str):
        resp = requests.put(
            self.main_url + 'resources',
            params={'path': folder_name},
            headers=self.main_headers
        )
        if resp.status_code == 409 or resp.status_code == 201:
            return True
        else:
            print(resp.json())
            return False

    def get_upload_link(self, folder_name: str, file_name: str):
        resp = requests.get(
            self.main_url + 'resources/upload',
            params={'path': folder_name + '/' + file_name, 'overwrite': 'true'},
            headers=self.main_headers
        )
        if resp.status_code == 200:
            href = resp.json()["href"]
            return href
        else:
            print(resp.json()['massage'])

    def upload_url(self, folder_name: str, file_name: str, url: str, file_format: str = '.jpg'):
        if self.create_folder(folder_name):
            href = self.get_upload_link(folder_name, file_name + file_format)
            image = requests.get(url)
            resp = requests.put(href, files={"file": image.content})
            if resp.status_code != 201:
                print(resp.json())
            else:
                return 'Файл загружен'

    def upload_file(self, folder_name: str, file_name: str, data, file_format: str = '.json'):
        if self.create_folder(folder_name):
            href = self.get_upload_link(folder_name, file_name + file_format)
            resp = requests.put(href, files={"file": data})
            if resp.status_code != 201:
                print(resp.json())
            else:
                return 'Файл загружен'

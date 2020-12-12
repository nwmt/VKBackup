import requests

with open('TOKEN.txt', encoding='utf-8') as file:
    TOKEN = file.read()


class VKUser:
    main_url = 'https://api.vk.com/method/'
    version = '5.126'
    params = {
        'access_token': TOKEN,
        'v': version}

    def __init__(self, user_id: int):
        self.user_id = user_id
        self.first_name = ''
        self.last_name = ''
        self.domain = ''
        self.has_photo = 0
        self.user_status = self.check_user()

    def __str__(self):
        return 'https://vk.com/' + self.domain

    def check_user(self):
        check_params = {'user_ids': self.user_id,
                        'fields': 'has_photo,domain'}
        response = requests.get(
            self.main_url + 'users.get',
            params={**self.params, **check_params})
        response.raise_for_status()
        response = response.json()
        if 'error' in response.keys():
            print(response['error']['error_msg'])
            return False
        self.first_name = response['response'][0]['first_name']
        self.last_name = response['response'][0]['last_name']
        self.has_photo = response['response'][0]['has_photo']
        self.domain = response['response'][0]['domain']
        if 'deactivated' in response['response'][0].keys():
            return False
        else:
            return not(response['response'][0]['is_closed'])

    def check_user_photos(self):
        if self.has_photo == 0:
            return False
        else:
            return True

    def get_profile_photos(self):
        if self.user_status and self.check_user_photos():
            profile_photo_params = {'owner_id': self.user_id,
                                    'album_id': 'profile',
                                    'rev': 0,
                                    'extended': 'likes'}
            response = requests.get(self.main_url + 'photos.get', params={**self.params, **profile_photo_params}).json()
            if 'response' in response.keys():
                result = response['response']['items']
                for i in result:
                    i['sizes'] = i['sizes'][-1]
                return result
            else:
                return response['error']['error_msg']
        else:
            return 'Error'

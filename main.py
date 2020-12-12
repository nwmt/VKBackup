import json
from os import listdir
from vk_user import VKUser
from ya_uploader import YaUploader
from datetime import datetime


def profile_photo_backup(who: int, how_much: int = 5):
    main_path = '/VKBackup_'
    user = VKUser(who)
    data = user.get_profile_photos()
    json_data = []
    if data == 'Error':
        print('Access error')
        return
    if how_much > len(data):
        how_much = len(data)
    elif len(data) == 0:
        print('User has no photos')
        return
    print(f'{user.first_name} {user.last_name} {str(user)} profile photos backup:')
    for i in range(how_much):
        owner_id = data[i]['owner_id']
        date = datetime.fromtimestamp(data[i]['date']).strftime("%m.%d.%Y %H_%M_%S")
        file_name = str(data[i]['likes']['count']) + ' likes ' + date
        YaUploader().upload_url(main_path + str(owner_id), file_name, data[i]['sizes']['url'])
        json_data.append({'file_name': file_name + '.jpg',
                          'size': data[i]['sizes']['type']})
        print(f'({i + 1}/{how_much}) - Uploading photo from {date} with {str(data[i]["likes"]["count"])} likes')
    print('Exporting JSON')
    YaUploader().upload_file(main_path + str(owner_id), str(owner_id) + '_profile_photos', json.dumps(json_data))
    print('Done')


def access_token(ya_token: str):
    with open('YA_TOKEN.txt', 'w', encoding='utf-8') as file:
        file.write(ya_token)


if __name__ == '__main__':
    if 'YA_TOKEN.txt' not in listdir():
        access_token(input('Enter Yandex.Disk access token: '))
    while True:
        inp = input('Enter vk.com user id: ')
        if inp == 'q':
            break
        count = input('Enter the number of photos (5 by default): ')
        if count != '':
            profile_photo_backup(int(inp), int(count))
        elif count == '':
            profile_photo_backup(int(inp))

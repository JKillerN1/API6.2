import random
import os
import vk_api
from vk_api import VkUpload
import requests
from dotenv import load_dotenv


def dowload_picture(filename, url):
    response = requests.get(url)
    response.raise_for_status()
    response = requests.get(response.json()['img'])
    with open(filename, 'wb') as file:
        file.write(response.content)



if __name__ == '__main__':
    load_dotenv()
    comic_number = random.randint (0,1000)
    filename = f'comic_img{comic_number}.png'
    url = f"https://xkcd.com/{comic_number}/info.0.json"

    try:
        dowload_picture(filename, url)

        login = os.getenv('LOGIN')
        password = os.getenv('PASSWORD')
        app_id = os.getenv('APP_ID')
        vk_session = vk_api.VkApi(login, password, app_id)
        vk_session.auth()
        upload = VkUpload(vk_session)
        photos = filename
        photo_list = upload.photo_wall(photos)
        attachment = ','.join('photo{owner_id}_{id}'.format(**item) for item in photo_list)
        vk_session.method("wall.post", {
            'owner_id': os.getenv('OWNER_ID'),
            'attachment': attachment,
        })

        os.remove(photos)

    except ValueError:
        os.remove(filename)


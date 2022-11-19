import random
import os
import vk_api
from vk_api import VkUpload
import requests
from dotenv import load_dotenv


def g(filename, url):
    response = requests.get(url)
    response.raise_for_status()
    x = response.json()['img']
    response = requests.get(x)
    with open(filename, 'wb') as file:
        file.write(response.content)


i = random.randint (0,1000)
filename2 = f'comic_img{i}.png'
url = f"https://xkcd.com/{i}/info.0.json"
g(filename2, url)

load_dotenv()
login = os.getenv('LOGIN')
password = os.getenv('PASSWORD')

app_id = os.getenv('APP_ID')
vk_session = vk_api.VkApi(login, password, app_id)
vk_session.auth()
upload = VkUpload(vk_session)
photos = filename2
photo_list = upload.photo_wall(photos)
attachment = ','.join('photo{owner_id}_{id}'.format(**item) for item in photo_list)
vk_session.method("wall.post", {
    'owner_id': os.getenv('OWNER_ID'),
    'attachment': attachment,
})
os.remove(photos)

import base64 
import os
from pprint import pprint
from time import sleep

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from zenrows import ZenRowsClient

groups = [
    {
        'name': 'Агата Кристи',
        'categories': 16902,
        'featured_media': 229994,
        'url': 'https://www.5lad.ru/akkordy/agata-kristi/',
    },
    {
        'name': 'Кино',
        'categories': 16905,
        'featured_media': 229999,
        'url': 'https://www.5lad.ru/akkordy/kino/',
    },
    {
        'name': 'Наутилус Помпилиус',
        'categories': 16906,
        'featured_media': 230000,
        'url': 'https://www.5lad.ru/akkordy/nautilus-pompilius/',
    },
    # {
    #     'name': 'Зиверт',
    #     'categories': 16907,
    #     'featured_media': 230001,
    #     'url': '',
    # },
]

cat = 16902 # agata kristi
donor_base_url = 'https://www.5lad.ru'

load_dotenv()
app_password = os.getenv('app_password')
base_endpoint = os.getenv('base_endpoint')
base_url = os.getenv('base_url')
sleep_time = int(os.getenv('sleep_time'))
user = 'poster'
credentials = user + ':' + app_password
token = base64.b64encode(credentials.encode())
header = {'Authorization': 'Basic ' + token.decode('utf-8')}
state_file = 'parser_state.dat'
last_page = 978306
api_key = '5465cb0010da8abfc214dfdeecd6026815e56b55'
client = ZenRowsClient(api_key)


def create_post(category_name, song_title, song_text, category_id, featured_media):
    url = f'{base_endpoint}/wp-json/wp/v2/posts'
    title = f"{category_name} - {song_title}"
    content = create_content(song_text)
    post = {
        'title': title,
        'content': content,
        'status': 'publish',
        'categories': category_id,
        'featured_media': featured_media,
    }
    response = requests.post(url , headers=header, json=post)
    return response


def create_content(song_text):
    content = f"""
        [wp_code id="1"]
        <pre class="qoate-code fontsize spacing chordcolor" id="ukutabs-song" data-key='A'>
        {song_text}
        </pre>
        [wp_code id="2"]
    """
    
    return content


def get_songs(url):
    songs_list = []
    response = client.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        main_div = soup.find('div', class_='lad-rightcolumn')
        songs = main_div.find_all('li')
        for song in songs:
            song_json = {}
            song_json['title'] = song.find('span').text
            song_json['url'] = donor_base_url + song.find('a')['href']
            songs_list.append(song_json)
        return songs_list
    else:
        print(f'Responde error: {response.status_code}')
        return False


def get_one_song(url):
    response = client.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        td = soup.find('td', class_='textofsong')
        song_text = td.find('pre').text
        return song_text
    else:
        print(response.status_code)
        return False


for group in groups:
    songs_list = get_songs(group['url'])
    for song in songs_list:
        song_text = get_one_song(song['url'])
        # print(group['name'])
        # print(group['categories'])
        # print(group['featured_media'])
        goup_name = group['name']
        song_title = song['title']
        print(f'Posting {goup_name} - {song_title}')
        # print(song_text)
        # print('='*50)
        create_post(group['name'], song['title'], song_text, group['categories'], group['featured_media'])
        sleep(1)


# response = create_post(post_json, category_json)
# pprint(response.json())

# songs_list = get_songs(groups[0]['url'])
# pprint(songs_list)

# song_text = get_one_song('https://www.5lad.ru/akkordy/agata-kristi/a-my-ne-angely-paren')
# print(song_text)
# coding=utf8
import os
from random import choice, sample

from imgurpython import ImgurClient

from slackbot.authentication import IMGUR_CLIENT_ID, IMGUR_CLIENT_SECRET, IMGUR_REFRESH_TOKEN
from slackbot.bot import respond_to

# needed to request images
client = ImgurClient(client_id=IMGUR_CLIENT_ID, client_secret=IMGUR_CLIENT_SECRET, refresh_token=IMGUR_REFRESH_TOKEN)

@respond_to(r'show me \<?(.*)\>?$')
def show_image(message, image_query):
    if ' png' in image_query:
        image_type = 'png'
    else:
        # make default gif
        image_type = 'anigif'

    items = client.gallery_search(q='', advanced={'q_type': image_type, 'q_all': image_query})
    # clear out non-image stuff
    items = [item for item in items if item.link.endswith('.{}'.format(image_type.replace('ani', '')))]
    # randomize what you see
    item = choice(items)
    message.reply(item.link)


@respond_to(r'\<?(.*)\>? bomb me \<?(\d+)\>?$')
def show_image_bomb(message, image_query, num_images):
    num_images = int(num_images)
    if ' png' in image_query:
        image_type = 'png'
    else:
        # make default gif
        image_type = 'anigif'

    items = client.gallery_search(q='', advanced={'q_type': image_type, 'q_all': image_query})
    # clear out non-image stuff
    items = [item for item in items if item.link.endswith('.{}'.format(image_type.replace('ani', '')))]
    # randomize what you see
    items = sample(items, num_images)
    for item in items:
        message.reply(item.link)

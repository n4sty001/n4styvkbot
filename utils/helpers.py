import aiohttp
import json

from .utils import Attachment
from .routine import traverse


async def upload_audio_message(api, multipart_data, peer_id):
    """Upload audio file `multipart_data` and return Attachment for sending to user with id `peer_id`(possibly)"""

    sender = api.get_default_sender("docs.getMessagesUploadServer")
    client = api.get_current_sender("docs.getMessagesUploadServer", sender=sender)

    data = aiohttp.FormData()
    data.add_field('file', multipart_data, filename="message.mp3", content_type='multipart/form-data')

    values = {'type': "audio_message", 'peer_id': peer_id}

    if client.group_id:
        values['group_id'] = client.group_id

    response = await api(sender=sender).docs.getMessagesUploadServer(**values)

    if not response or not response.get('upload_url'):
        return None

    upload_url = response['upload_url']

    async with aiohttp.ClientSession() as sess:
        async with sess.post(upload_url, data=data) as resp:
            result = json.loads(await resp.text())

    if not result:
        return None

    data = dict(file=result['file'])
    result = await api(sender=sender).docs.save(**data)

    if not result:
        return None

    return Attachment.from_upload_result(result[0], "doc")

async def upload_graffiti(api, multipart_data, filename):
    return await upload_doc(api, multipart_data, filename, {"type": "graffiti"})

async def upload_doc(api, multipart_data, filename="image.png", additional_params=None):
    """Upload file `multipart_data` and return Attachment for sending to user"""

    if additional_params is None:
        additional_params = {}

    sender = api.get_default_sender("docs.getWallUploadServer")
    client = api.get_current_sender("docs.getWallUploadServer", sender=sender)

    data = aiohttp.FormData()
    data.add_field('file', multipart_data, filename=filename,
        content_type='multipart/form-data')

    values = {}
    values.update(additional_params)

    if client.group_id:
        values['group_id'] = client.group_id

    response = await api(sender=sender).docs.getWallUploadServer(**values)

    if not response or not response.get('upload_url'):
        return None

    upload_url = response['upload_url']

    async with aiohttp.ClientSession() as sess:
        async with sess.post(upload_url, data=data) as resp:
            result = json.loads(await resp.text())

    if not result or not result.get("file"):
        print(result)
        return None

    data = dict(file=result['file'])
    result = await api(sender=sender).docs.save(**data)

    if not result:
        return None

    return Attachment.from_upload_result(result[0], "doc")


async def upload_photo(api, multipart_data, peer_id=None):
    """Upload photo file `multipart_data` and return Attachment for sending to
    user with id `peer_id`(optional but recommended)"""

    sender = api.get_default_sender('photos.getMessagesUploadServer')

    data = aiohttp.FormData()
    data.add_field('photo', multipart_data, filename='picture.png',
        content_type='multipart/form-data')

    if peer_id:
        kwargs = {"peer_id": peer_id}
    else:
        kwargs = {}

    response = await api(sender=sender).photos.getMessagesUploadServer(**kwargs)

    if not response or not response.get('upload_url'):
        return None

    upload_url = response['upload_url']

    async with aiohttp.ClientSession() as sess:
        async with sess.post(upload_url, data=data) as resp:
            result = json.loads(await resp.text())

    if not result:
        return None

    result = await api(sender=sender).photos.saveMessagesPhoto(
        **{'photo': result['photo'], 'hash': result['hash'], 'server': result['server']})

    if not result:
        return None

    return Attachment.from_upload_result(result[0])

async def parse_user_name(user_id, entity):
    """Entitty is Message or Event"""

    if entity:
        if entity.meta.get("user_info"):
            u = entity.meta["user_info"]["raw"]

            if u and u["id"] == user_id:
                return u["first_name"] + " " + u["last_name"]

        if entity.meta.get("data_chat") and entity.meta["data_chat"].get("chat_info"):
            for u in entity.meta["data_chat"]["chat_info"]["users"]:
                if u and u["id"] == user_id:
                    return u["first_name"] + " " + u["last_name"]

    us = await entity.api.users.get(user_ids=user_id, fields="sex,screen_name,nickname")

    if not us:
        return str(user_id)

    return us[0]["first_name"] + " " + us[0]["last_name"]

async def parse_user_id(msg, can_be_argument=True, argument_ind=-1, custom_text=None):
    """Returns specified in messages user's id if possible."""

    for m in traverse(await msg.get_full_forwarded()):
        if m.user_id and m.true_user_id != msg.user_id:
            return m.true_user_id

    if not can_be_argument:
        return None

    if custom_text is None:
        original_text = msg.text
    else:
        original_text = custom_text

    text = original_text.split(" ")[argument_ind]

    if text.isdigit():
        return int(text)

    if text.startswith("https://vk.com/"):
        text = text[15:]

    if text[:3] == "[id":
        puid = text[3:].split("|")[0]

        if puid.isdigit() and "]" in text[3:]:
            return int(puid)

    if msg.meta.get("data_chat") and "chat_info" in msg.meta["data_chat"]:
        if argument_ind == -1:
            targets = [original_text.split(" ")[-1].strip().lower()]
        else:
            targets = [i.strip().lower() for i in original_text.split(" ")[argument_ind: argument_ind + 2]]

        max_match, user_id = 0, None
        for u in msg.meta["data_chat"]["chat_info"]["users"] + \
                msg.meta["data_chat"]["chat_info"]["prev_users"]:
            if u.get("screen_name") == text:
                return u["id"]

            matches = 0
            if u.get("first_name", "").strip().lower() in targets:
                matches += 1
            if u.get("last_name", "").strip().lower() in targets:
                matches += 1
            if u.get("nickname", "").strip().lower() in targets:
                matches += 1

            if matches > 0:
                if matches > max_match:
                    max_match = matches
                    user_id = u["id"]

                elif matches == max_match:
                    user_id = None
                    break

        if user_id is not None:
            return user_id

    tuid = await msg.api.utils.resolveScreenName(screen_name=text)

    if tuid and isinstance(tuid, dict):
        return tuid.get("object_id")

    return None

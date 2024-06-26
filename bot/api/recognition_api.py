import json
from typing import List, cast

import aiohttp
from aiohttp import ClientResponse, web
from aiohttp.web_response import Response

from bot.config import settings
from bot.model.face_location import FaceLocation
from bot.model.image import Image

headers = {
    'Authorization': 'Bearer ' + settings.api.token
}


async def get_all_person_names(user_id: int) -> list[str]:
    async with aiohttp.ClientSession() as session:
        async with session.get(settings.api.base_url + settings.api.face_recognition_prefix + "/person/get/all",
                               params={'client_id': user_id},
                               headers=headers) as response:
            return await response.json()


async def recognize_image(user_id: str,
                          key: str,
                          face_locations: List[FaceLocation] | None = None):
    async with aiohttp.ClientSession() as session:
        async with session.post(settings.api.base_url + settings.api.face_recognition_prefix + "/image/recognize",
                                params={'client_id': user_id,
                                        'key': key},
                                data={'face_locations': [fl.to_dict() for fl in
                                                         face_locations] if face_locations is not None else []},
                                headers=headers) as response:
            return response


async def get_images_by_person_name(user_id: int, person_name: str) -> list[Image]:
    async with aiohttp.ClientSession() as session:
        async with session.get(settings.api.base_url + settings.api.face_recognition_prefix + "/image/get/",
                               params={'client_id': user_id,
                                       'person_name': person_name},
                               headers=headers) as response:
            return [Image(id=image['id'], key=image['key']) for image in await response.json()]


async def delete_person(user_id: int, person_name: str) -> ClientResponse:
    async with aiohttp.ClientSession() as session:
        async with session.delete(settings.api.base_url + settings.api.face_recognition_prefix + "/person/delete/",
                                  params={'client_id': user_id,
                                          'person_name': person_name},
                                  headers=headers) as response:
            return response


async def delete_image(user_id: int, image_id: int) -> ClientResponse:
    async with aiohttp.ClientSession() as session:
        async with session.delete(settings.api.base_url + settings.api.face_recognition_prefix + "/image/delete/",
                                  params={'client_id': user_id,
                                          'image_id': image_id},
                                  headers=headers) as response:
            return response


async def set_image(user_id: str, person_name: str, key: str) -> ClientResponse:
    async with aiohttp.ClientSession() as session:
        async with session.post(settings.api.base_url + settings.api.face_recognition_prefix + "/image/set",
                                params={'client_id': user_id,
                                        'person_name': person_name,
                                        'key': key},
                                headers=headers) as response:
            return response

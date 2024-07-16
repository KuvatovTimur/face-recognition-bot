from io import BytesIO

import aioboto3
from aioboto3 import Session
from aiogram import Bot
from aiogram.types import PhotoSize

from bot.config import settings

bot = Bot(
        token=settings.bot.token,
    )

async def s3_put_image(
        image: PhotoSize,
        key: str,
        content_type: str
):
    file = await bot.get_file(image.file_id)
    file_bytes = await bot.download_file(file.file_path)
    session_instance = aioboto3.Session()
    async with session_instance.client(service_name="s3", endpoint_url=settings.s3.endpoint,
                                       aws_access_key_id=settings.s3.key_id,
                                       aws_secret_access_key=settings.s3.access_key,
                                       region_name=settings.s3.region_name) as s3:
        await s3.put_object(Body=file_bytes, Bucket=settings.s3.basket_name, ContentType=content_type, Key=key)




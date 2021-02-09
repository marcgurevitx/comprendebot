from aiobotocore import get_session
from botocore.exceptions import ClientError

from botcommon.config import config


async def save_binary(key, binary):
    session = get_session()
    client_creator = session.create_client(
        "s3",
        endpoint_url=config.S3_URL,
        aws_access_key_id=config.S3_ACCESS_KEY,
        aws_secret_access_key=config.S3_SECRET_KEY,
    )
    async with client_creator as client:
        try:
            await client.create_bucket(Bucket=config.S3_VOICES_BUCKET)
        except ClientError:
            pass
        await client.put_object(Bucket=config.S3_VOICES_BUCKET, Key=key, Body=binary)


async def retrieve_binary(key):
    session = get_session()
    client_creator = session.create_client(
        "s3",
        endpoint_url=config.S3_URL,
        aws_access_key_id=config.S3_ACCESS_KEY,
        aws_secret_access_key=config.S3_SECRET_KEY,
    )
    async with client_creator as client:
        response = await client.get_object(Bucket=config.S3_VOICES_BUCKET, Key=key)
        async with response["Body"] as stream:
            return await stream.read()

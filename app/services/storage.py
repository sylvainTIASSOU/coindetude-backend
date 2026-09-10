"""Client de stockage Cloudflare R2 (API compatible S3).

boto3 est synchrone : les appels sont donc délégués à un threadpool via
`run_in_threadpool` pour ne pas bloquer la boucle asyncio. Si le volume
d'IO stockage devient significatif, envisager `aioboto3` en V2.
"""

from functools import lru_cache

import boto3
from botocore.client import Config
from fastapi.concurrency import run_in_threadpool

from app.core.config import settings


@lru_cache
def _client():  # type: ignore[no-untyped-def]
    return boto3.client(
        "s3",
        endpoint_url=settings.R2_ENDPOINT_URL,
        aws_access_key_id=settings.R2_ACCESS_KEY_ID,
        aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
        config=Config(signature_version="s3v4"),
        region_name="auto",
    )


async def upload_file(key: str, content: bytes, content_type: str) -> str:
    """Upload et retourne la clé de l'objet stocké."""
    await run_in_threadpool(
        _client().put_object,
        Bucket=settings.R2_BUCKET_NAME,
        Key=key,
        Body=content,
        ContentType=content_type,
    )
    return key


async def get_presigned_url(key: str, expires_in: int = 3600) -> str:
    """URL signée temporaire — pour servir un PDF sans exposer le bucket publiquement."""
    return await run_in_threadpool(
        _client().generate_presigned_url,
        ClientMethod="get_object",
        Params={"Bucket": settings.R2_BUCKET_NAME, "Key": key},
        ExpiresIn=expires_in,
    )

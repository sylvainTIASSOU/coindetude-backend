"""Client S3 async (compatible MinIO, Cloudflare R2, AWS S3).

Utilise ``aioboto3`` pour rester non-bloquant côté FastAPI.

Configuration via ``Settings`` : ``S3_ENDPOINT_URL``, ``S3_ACCESS_KEY_ID``,
``S3_SECRET_ACCESS_KEY``, ``S3_BUCKET_NAME``, ``S3_REGION``.
"""

from __future__ import annotations


from typing import Any

import aioboto3
from botocore.exceptions import ClientError

from app.core.config import settings

from app.core.logging import log as logger


class S3Client:
    """Wrapper minimal autour d'aioboto3 pour les opérations presign + head."""

    def __init__(self) -> None:
        self._session = aioboto3.Session()
        self.bucket = settings.S3_BUCKET_NAME

    def _client_kwargs(self) -> dict[str, Any]:
        kwargs: dict[str, Any] = {
            "region_name": settings.S3_REGION,
            "aws_access_key_id": settings.S3_ACCESS_KEY_ID,
            "aws_secret_access_key": settings.S3_SECRET_ACCESS_KEY,
        }
        if settings.S3_ENDPOINT_URL:
            kwargs["endpoint_url"] = settings.S3_ENDPOINT_URL
        return kwargs

    async def presign_put(
        self,
        *,
        key: str,
        content_type: str,
        expires_in: int | None = None,
    ) -> str:
        """Génère une URL pré-signée PUT pour upload direct.

        Le client doit envoyer le même ``Content-Type`` que celui signé,
        sinon S3 rejette la requête (SignatureDoesNotMatch).
        """
        expires = expires_in or settings.UPLOAD_PRESIGN_TTL_SECONDS
        async with self._session.client("s3", **self._client_kwargs()) as s3:
            url: str = await s3.generate_presigned_url(
                ClientMethod="put_object",
                Params={
                    "Bucket": self.bucket,
                    "Key": key,
                    "ContentType": content_type,
                },
                ExpiresIn=expires,
                HttpMethod="PUT",
            )
        return url

    async def presign_get(
        self,
        *,
        key: str,
        expires_in: int | None = None,
    ) -> str:
        """Génère une URL pré-signée GET pour lecture."""
        expires = expires_in or settings.UPLOAD_GET_TTL_SECONDS
        async with self._session.client("s3", **self._client_kwargs()) as s3:
            url: str = await s3.generate_presigned_url(
                ClientMethod="get_object",
                Params={"Bucket": self.bucket, "Key": key},
                ExpiresIn=expires,
                HttpMethod="GET",
            )
        return url

    async def head_object(self, *, key: str) -> dict[str, Any] | None:
        """Retourne les métadonnées d'un objet, ou None s'il n'existe pas."""
        try:
            async with self._session.client("s3", **self._client_kwargs()) as s3:
                meta: dict[str, Any] = await s3.head_object(
                    Bucket=self.bucket, Key=key
                )
                return meta
        except ClientError as exc:
            code = exc.response.get("Error", {}).get("Code", "")
            if code in ("404", "NoSuchKey", "NotFound"):
                return None
            logger.error("head_object échec pour %s : %s", key, exc)
            raise

    async def delete_object(self, *, key: str) -> None:
        """Supprime un objet (idempotent : ne lève pas si absent)."""
        try:
            async with self._session.client("s3", **self._client_kwargs()) as s3:
                await s3.delete_object(Bucket=self.bucket, Key=key)
        except ClientError as exc:
            logger.warning("delete_object échec pour %s : %s", key, exc)

    async def ensure_bucket_exists(self) -> None:
        """Crée le bucket s'il n'existe pas (utile en dev MinIO)."""
        try:
            async with self._session.client("s3", **self._client_kwargs()) as s3:
                try:
                    await s3.head_bucket(Bucket=self.bucket)
                    logger.info("Bucket S3 '%s' déjà présent.", self.bucket)
                except ClientError:
                    await s3.create_bucket(Bucket=self.bucket)
                    logger.info("Bucket S3 '%s' créé.", self.bucket)
        except Exception as exc:  # noqa: BLE001
            logger.warning("ensure_bucket_exists échec : %s", exc)


_s3_client: S3Client | None = None


def get_s3_client() -> S3Client:
    """Retourne le client S3 partagé (création paresseuse)."""
    global _s3_client
    if _s3_client is None:
        _s3_client = S3Client()
    return _s3_client

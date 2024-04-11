# mypy: disable-error-code="misc"

from typing import cast

from fastapi_storages import S3Storage as _S3Storage

from app.core.config import settings

MINIO_ACCESS_KEY = settings.MINIO_USER
MINIO_SECRET_KEY = settings.MINIO_PASSWORD
MINIO_BUCKET = settings.MINIO_BUCKET
MINIO_HOST = settings.MINIO_HOST
MINIO_PORT = settings.MINIO_PORT
MINIO_URL = f"{MINIO_HOST}:{MINIO_PORT}"


class S3Storage(_S3Storage):
    def get_path(self, name: str) -> str:
        """
        Get full URL to the file.
        """

        key = self.get_name(name)

        if self.AWS_S3_CUSTOM_DOMAIN:
            return f"{self._http_scheme}://{self.AWS_S3_CUSTOM_DOMAIN}/{key}"

        if self.AWS_QUERYSTRING_AUTH:
            params = {"Bucket": self._bucket.name, "Key": key}
            return cast(
                str,
                self._s3.meta.client.generate_presigned_url(
                    "get_object", Params=params, ExpiresIn=3600
                ),
            )

        return f"{self._http_scheme}://{self.AWS_S3_ENDPOINT_URL}/{self.AWS_S3_BUCKET_NAME}/{key}"


class PublicAssetS3Storage(S3Storage):
    AWS_ACCESS_KEY_ID = MINIO_ACCESS_KEY
    AWS_SECRET_ACCESS_KEY = MINIO_SECRET_KEY
    AWS_S3_BUCKET_NAME = MINIO_BUCKET
    AWS_S3_ENDPOINT_URL = MINIO_URL
    AWS_DEFAULT_ACL = "public-read"
    AWS_S3_USE_SSL = False
    AWS_QUERYSTRING_AUTH = True


storage = PublicAssetS3Storage()

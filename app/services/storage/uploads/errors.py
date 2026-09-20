"""Erreurs du module uploads."""

from __future__ import annotations


class UploadError(Exception):
    def __init__(self, detail: str, status_code: int = 400) -> None:
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)


class UploadPolicyError(UploadError):
    def __init__(self, detail: str) -> None:
        super().__init__(detail, status_code=422)


class FileNotFoundError_(UploadError):
    def __init__(self, detail: str = "Fichier introuvable.") -> None:
        super().__init__(detail, status_code=404)


class FileAlreadyConfirmed(UploadError):
    def __init__(self) -> None:
        super().__init__(
            "Ce fichier a déjà été confirmé.", status_code=409
        )


class FileNotUploadedToStorage(UploadError):
    def __init__(self) -> None:
        super().__init__(
            "L'objet n'existe pas sur le stockage. "
            "L'upload a-t-il bien été effectué ?",
            status_code=409,
        )


class FileSizeMismatch(UploadError):
    def __init__(self, declared_kb: int, actual_kb: int, max_kb: int) -> None:
        super().__init__(
            f"Taille réelle ({actual_kb} KB) ≠ déclarée ({declared_kb} KB) "
            f"ou dépasse la limite ({max_kb} KB).",
            status_code=422,
        )

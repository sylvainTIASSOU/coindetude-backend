"""Erreurs du module students."""

from __future__ import annotations


class StudentError(Exception):
    def __init__(self, detail: str, status_code: int = 400) -> None:
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)


class NotAStudentError(StudentError):
    def __init__(self) -> None:
        super().__init__(
            "Cet utilisateur n'est pas un élève.", status_code=403
        )


class ProfileNotFoundError(StudentError):
    def __init__(self) -> None:
        super().__init__("Profil élève introuvable.", status_code=404)


class LevelNotFoundError(StudentError):
    def __init__(self, name: str, cycle: str) -> None:
        super().__init__(
            f"Niveau '{name}' introuvable pour le cycle '{cycle}'.",
            status_code=404,
        )


class SeriesNotFoundError(StudentError):
    def __init__(self, code: str, cycle: str) -> None:
        super().__init__(
            f"Série '{code}' introuvable pour le cycle '{cycle}'.",
            status_code=404,
        )


class SeriesNotAllowedForLevelError(StudentError):
    def __init__(self, series_code: str, level_name: str) -> None:
        super().__init__(
            f"La série '{series_code}' n'est pas proposée en "
            f"'{level_name}'. Vérifie le niveau choisi.",
            status_code=422,
        )


class NotGuardianError(StudentError):
    def __init__(self) -> None:
        super().__init__(
            "Tu n'as pas accès au profil de cet élève.", status_code=403
        )
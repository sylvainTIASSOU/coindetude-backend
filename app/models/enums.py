"""Enums PostgreSQL partagés entre les modèles CoinDetude.

Chaque enum est matérialisé en base comme un type PostgreSQL natif
(``CREATE TYPE ... AS ENUM``). Cela garantit l'intégrité des données
et facilite les migrations ultérieures.

⚠️ Convention : les valeurs sont en ``snake_case`` minuscule pour rester
compatibles avec les payloads JSON du frontend Flutter.
"""

from __future__ import annotations

import enum
from sqlalchemy import Enum as SAEnum

class UserRole(str, enum.Enum):  # noqa: UP042
    """Rôle d'un utilisateur dans la plateforme."""

    STUDENT = "student"
    PARENT = "parent"
    TEACHER = "teacher"
    ADMIN = "admin"


class FileContext(str, enum.Enum):
    """Contexte d'usage d'un fichier uploadé."""

    AVATAR = "avatar"
    RESOURCE_PDF = "resource_pdf"
    AI_SCAN = "ai_scan"


class Platform(str, enum.Enum):
    """Plateforme d'un device enregistré pour les push notifications."""

    ANDROID = "android"
    IOS = "ios"
    WEB = "web"


class NotificationType(str, enum.Enum):
    """Catégorie d'une notification envoyée."""

    REMINDER = "reminder"
    SYSTEM = "system"
    RESULT = "result"
    NEWS = "news"
    OTHER = "other"


class Cycle(str, enum.Enum):
    """Cycle d'enseignement au Togo.

    Le lycée est scindé en deux types car les séries, les programmes et les
    examens diffèrent :
    - ``lycee_moderne`` : séries générales (A4, C, D, E...)
    - ``lycee_technique`` : séries techniques (F1, F2, F3, F4...)
    """

    COLLEGE = "college"
    LYCEE_MODERNE = "lycee_moderne"
    LYCEE_TECHNIQUE = "lycee_technique"


class ResourceType(str, enum.Enum):
    """Type de ressource pédagogique."""

    COURS = "cours"
    EXERCICE = "exercice"
    ANNALE = "annale"
    CORRIGE = "corrige"


class ResourceOrigin(str, enum.Enum):
    """Source d'une ressource pédagogique."""

    ADMIN = "admin"
    TEACHER = "teacher"
    IA = "ia"


class AIRole(str, enum.Enum):
    """Rôle d'un message dans une conversation IA."""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class PlanningEventType(str, enum.Enum):
    """Type d'événement dans le planning personnel d'un élève."""

    REVISION = "revision"
    EXAM = "exam"
    DEVOIR = "devoir"
    RENTREE = "rentree"
    COMPOSITION = "composition"
    HOMEWORK = "homework"
    AUTRE = "autre"


class CalendarEventType(str, enum.Enum):
    """Type d'événement dans le calendrier national officiel."""

    RENTREE = "rentree"
    EXAMEN = "examen"
    CONGE = "conge"
    RESULTAT = "resultat"
    AUTRE = "autre"


class PlanType(str, enum.Enum):
    """Type de forfait Mobile Money."""

    FREEMIUM = "freemium"
    PASS_JOUR = "pass_jour"
    PASS_SEMAINE = "pass_semaine"
    PASS_MOIS = "pass_mois"


class PaymentProvider(str, enum.Enum):
    """Opérateur Mobile Money utilisé pour un paiement."""

    TMONEY = "tmoney"
    FLOOZ = "flooz"
    CARD = "card"
    CASH = "cash"


class TransactionStatus(str, enum.Enum):
    """Statut d'une transaction Mobile Money."""

    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"


class TeacherVerificationStatus(str, enum.Enum):
    """Statut de vérification d'un compte enseignant (Marketplace V2)."""

    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"


class SyncOperation(str, enum.Enum):
    """Opération CRDT envoyée par un client offline-first."""

    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"


class ConflictStrategy(str, enum.Enum):
    """Stratégie de résolution de conflit côté serveur."""

    SERVER_AUTHORITATIVE = "SERVER_AUTHORITATIVE"
    CRDT_MERGE = "CRDT_MERGE"
    LWW = "LWW"
    MANUAL = "MANUAL"

class OTPPurpose(str, enum.Enum):
    """Raison d'émission d'un code OTP."""
    REGISTER = "register"
    LOGIN = "login"
    RESET_PASSWORD = "reset_password"


class OTPChannel(str, enum.Enum):
    """Canal de livraison du code OTP."""
    WHATSAPP = "whatsapp"
    SMS = "sms"

class SyncEntityType(str, enum.Enum):
    """Types d'entités supportés par /sync/apply-event."""
    PLANNING_TASK = "planning_task"
    XP_EVENT = "xp_event"
    STREAK_EVENT = "streak_event"


class UserEventKind(str, enum.Enum):
    """Nature d'un événement CRDT additif."""
    XP_ADDED = "xp_added"
    STREAK_DAY = "streak_day"

class FileStatus(str, enum.Enum):
    """Statut d'un fichier dans son cycle de vie."""
    PENDING = "pending"       # Row créée, upload S3 pas encore confirmé
    UPLOADED = "uploaded"     # Confirmé, prêt à l'emploi
    FAILED = "failed"         # Upload invalide (taille/type), à nettoyer


class UploadPurpose(str, enum.Enum):
    """Purpose déclaré par le client au presign."""
    AVATAR = "avatar"
    HOMEWORK_SCAN = "homework_scan"
    RESOURCE_PDF = "resource_pdf"

def pg_enum(enum_cls: type[enum.Enum], name: str) -> SAEnum:
    """Crée un type ENUM PostgreSQL natif à partir d'un Enum Python.

    Force l'utilisation des **valeurs** (``e.value``) plutôt que des **noms**
    (``e.name``). Indispensable pour rester compatible avec les payloads JSON
    du client Flutter qui sérialise ``UserRole.STUDENT`` en ``"student"``.

    Args:
        enum_cls: Classe Enum Python (héritant de ``str, enum.Enum``).
        name: Nom du type PostgreSQL (ex: ``"user_role"``).

    Returns:
        Instance ``sqlalchemy.Enum`` configurée pour PostgreSQL natif.
    """
    return SAEnum(
        enum_cls,
        name=name,
        native_enum=True,
        create_constraint=False,  # Pas de CHECK constraint, PG gère le type
        values_callable=lambda x: [e.value for e in x], # type: ignore
        validate_strings=True,
    )

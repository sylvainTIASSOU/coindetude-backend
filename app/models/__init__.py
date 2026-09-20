"""Modèles SQLAlchemy de CoinDetude (exports centralisés)."""

from app.models.ai import AIConversation, AIMessage, StudyFiche
from app.models.auth import IdempotencyKey, RefreshToken
from app.models.base import Base, TimestampMixin, UUIDMixin
from app.models.calendar import NationalCalendar, StudyPlanning
from app.models.educational import (
    Chapter,
    Level,
    LevelSeries,
    Series,
    Subject,
)
from app.models.enums import (
    AIRole,
    CalendarEventType,
    ConflictStrategy,
    Cycle,
    FileContext,
    NotificationType,
    OTPChannel,
    OTPPurpose,
    PaymentProvider,
    PlanningEventType,
    PlanType,
    Platform,
    ResourceOrigin,
    ResourceType,
    SyncEntityType,
    SyncOperation,
    TeacherVerificationStatus,
    TransactionStatus,
    UserEventKind,
    UserRole,
    FileStatus,
    UploadPurpose,
    pg_enum,
)
from app.models.file import StoredFile
from app.models.notification import (
    DeviceToken,
    NotificationPreference,
    SentNotification,
)
from app.models.otp import OTPCode
from app.models.payment import Subscription, Transaction
from app.models.plan import Plan
from app.models.quiz import Quiz, QuizAttempt, QuizQuestion
from app.models.resource import Resource
from app.models.trusted_device import TrustedDevice
from app.models.user import (
    ParentProfile,
    ParentStudent,
    StudentProfile,
    TeacherProfile,
    User,
)
from app.models.user_event import UserEvent

__all__ = [
    # Base & mixins
    "Base",
    "UUIDMixin",
    "TimestampMixin",
    # Enums
    "AIRole",
    "CalendarEventType",
    "ConflictStrategy",
    "Cycle",
    "FileContext",
    "NotificationType",
    "PaymentProvider",
    "PlanType",
    "Platform",
    "PlanningEventType",
    "ResourceOrigin",
    "ResourceType",
    "SyncOperation",
    "TeacherVerificationStatus",
    "TransactionStatus",
    "UserRole",
    "pg_enum",
    # User & profils
    "User",
    "StudentProfile",
    "ParentProfile",
    "TeacherProfile",
    "ParentStudent",
    # Auth
    "RefreshToken",
    "IdempotencyKey",
    # Éducatif
    "Level",
    "Series",
    "LevelSeries",
    "Subject",
    "Chapter",
    # Fichiers
    "StoredFile",
    # Notifications
    "DeviceToken",
    "NotificationPreference",
    "SentNotification",
    # IA
    "AIConversation",
    "AIMessage",
    "StudyFiche",
    # Quiz
    "Quiz",
    "QuizQuestion",
    "QuizAttempt",
    # Calendrier
    "StudyPlanning",
    "NationalCalendar",
    # Paiement
    "Subscription",
    "Transaction",
    # Ressources & plans
    "Resource",
    "Plan",
    # ...
    "OTPCode",
    "OTPPurpose",
    "OTPChannel",
    "TrustedDevice",
    # ...
    # ...
    "UserEvent",
    "SyncEntityType",
    "UserEventKind",
    "FileStatus",
    "UploadPurpose",
]

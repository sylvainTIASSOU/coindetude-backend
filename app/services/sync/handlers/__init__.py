"""Registre des handlers par type d'entité."""

from app.models.enums import SyncEntityType
from app.services.sync.handlers.base import SyncHandler
from app.services.sync.handlers.planning_task import PlanningTaskHandler
from app.services.sync.handlers.streak_event import StreakEventHandler
from app.services.sync.handlers.xp_event import XPEventHandler

HANDLERS: dict[SyncEntityType, type[SyncHandler]] = {
    SyncEntityType.PLANNING_TASK: PlanningTaskHandler,
    SyncEntityType.XP_EVENT: XPEventHandler,
    SyncEntityType.STREAK_EVENT: StreakEventHandler,
}

__all__ = ["HANDLERS", "SyncHandler"]

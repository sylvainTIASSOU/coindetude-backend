"""Schémas Pydantic v2 pour la ressource User (entrée/sortie API)."""

import uuid

from pydantic import BaseModel, ConfigDict, EmailStr

from app.models.user import UserRole


class UserBase(BaseModel):
    email: EmailStr
    full_name: str


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)  # permet .model_validate(orm_obj)

    id: uuid.UUID
    role: UserRole
    is_active: bool

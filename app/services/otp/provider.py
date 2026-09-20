"""Providers de livraison OTP (WhatsApp + SMS)."""

from __future__ import annotations

import abc
from typing import Any

import httpx

from app.core.config import settings
from app.core.logging import log as logger
from app.models.enums import OTPChannel, OTPPurpose


class OTPProvider(abc.ABC):
    """Interface abstraite pour l'envoi d'OTP."""

    @abc.abstractmethod
    async def send(self, *, phone: str, code: str, purpose: OTPPurpose, channel: OTPChannel) -> str:
        """Envoie le code et retourne l'ID message du provider."""


class ConsoleOTPProvider(OTPProvider):
    """Provider de développement : ne fait rien, loggue le code."""

    async def send(self, *, phone: str, code: str, purpose: OTPPurpose, channel: OTPChannel) -> str:
        logger.warning(
            "🔐 [CONSOLE OTP] to=%s channel=%s purpose=%s code=%s",
            phone,
            channel.value,
            purpose.value,
            code,
        )
        return f"console-{purpose.value}-{phone[-4:]}"


class AfricasTalkingProvider(OTPProvider):
    """Provider Africa's Talking (SMS + WhatsApp Business).

    Doc : https://developers.africastalking.com/
    """

    SMS_URL = "https://api.africastalking.com/version1/messaging"
    WHATSAPP_URL = "https://chat.africastalking.com/whatsapp/message"

    def __init__(self) -> None:
        self.username = settings.AT_USERNAME
        self.api_key = settings.AT_API_KEY

    def _headers(self) -> dict[str, str]:
        return {
            "apiKey": self.api_key,
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }

    def _message(self, code: str) -> str:
        return (
            f"CoinDetude : votre code de vérification est {code}. "
            "Il expire dans 5 minutes. Ne le partagez jamais."
        )

    async def send(self, *, phone: str, code: str, purpose: OTPPurpose, channel: OTPChannel) -> str:
        message = self._message(code)
        async with httpx.AsyncClient(timeout=10.0) as client:
            if channel is OTPChannel.WHATSAPP:
                payload: dict[str, Any] = {
                    "username": self.username,
                    "to": phone,
                    "from": settings.AT_WHATSAPP_SENDER or "",
                    "message": message,
                }
                resp = await client.post(self.WHATSAPP_URL, data=payload, headers=self._headers())
            else:
                payload = {
                    "username": self.username,
                    "to": phone,
                    "from": settings.AT_SENDER_ID,
                    "message": message,
                }
                resp = await client.post(self.SMS_URL, data=payload, headers=self._headers())
            resp.raise_for_status()
            data = resp.json()

        # AT retourne des structures différentes selon SMS/WhatsApp
        try:
            if channel is OTPChannel.WHATSAPP:
                return str(data.get("messageId", data.get("id", "unknown")))
            recipients = data["SMSMessageData"]["Recipients"]
            return str(recipients[0].get("messageId", "unknown"))
        except (KeyError, IndexError):
            logger.warning("Réponse AT inattendue : %s", data)
            return "unknown"


def get_otp_provider() -> OTPProvider:
    """Retourne le provider actif selon la config."""
    if settings.ENVIRONMENT == "dev" or settings.OTP_FORCE_CONSOLE:
        return ConsoleOTPProvider()
    return AfricasTalkingProvider()

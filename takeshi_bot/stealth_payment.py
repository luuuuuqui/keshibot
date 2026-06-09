from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any

from takeshi_bot import config
from takeshi_bot.bridge import BaileysBridge
from takeshi_bot.database import read_group_restrictions
from takeshi_bot.logger import error_log, warning_log
from takeshi_bot.message_handler import apply_anti_payment_restriction

CIPHERTEXT_STUB = 2
REPEAT_WINDOW_MS = 2 * 60 * 1000
ALERT_COOLDOWN_MS = 5 * 60 * 1000
TRACKER_TTL_MS = 10 * 60 * 1000


@dataclass
class TrackerEntry:
    count: int
    window_start: int
    last_alert_at: int = 0


tracker: dict[str, TrackerEntry] = {}
last_sweep = int(time.time() * 1000)


def _now_ms() -> int:
    return int(time.time() * 1000)


def _sweep(now: int) -> None:
    global last_sweep
    if now - last_sweep < TRACKER_TTL_MS:
        return
    last_sweep = now
    expired = [
        key for key, entry in tracker.items() if now - entry.window_start > TRACKER_TTL_MS
    ]
    for key in expired:
        tracker.pop(key, None)


def _register_failure(key: str, now: int) -> TrackerEntry:
    entry = tracker.get(key)
    if entry is None or now - entry.window_start > REPEAT_WINDOW_MS:
        entry = TrackerEntry(count=0, window_start=now)
    entry.count += 1
    tracker[key] = entry
    return entry


def _on_cooldown(entry: TrackerEntry, now: int) -> bool:
    return bool(entry.last_alert_at and now - entry.last_alert_at < ALERT_COOLDOWN_MS)


def _confidence(web_message: dict[str, Any]) -> str | None:
    meta = web_message.get("stealthMeta") or {}
    if meta.get("decryptFail") == "hide":
        return "high"
    return None


def _short_jid(jid: str) -> str:
    return (jid or "desconhecido").split("@")[0].split(":")[0]


async def _sender_is_exempt(
    bridge: BaileysBridge, remote_jid: str, sender: str
) -> bool:
    if sender in {config.OWNER_LID, config.BOT_LID}:
        return True
    try:
        metadata = await bridge.group_metadata(remote_jid)
    except Exception as error:
        warning_log(f"[stealth-payment] Falha ao obter metadados: {error}")
        return False
    participant = next(
        (item for item in metadata.get("participants", []) if item.get("id") == sender),
        None,
    )
    if not participant:
        return False
    return (
        sender == metadata.get("owner")
        or participant.get("admin") == "superadmin"
        or participant.get("admin") == "admin"
    )


async def handle_stealth_payment_detection(
    bridge: BaileysBridge, web_message: dict[str, Any]
) -> None:
    try:
        key = web_message.get("key") or {}
        if not key or key.get("fromMe"):
            return
        remote_jid = key.get("remoteJid")
        if not remote_jid or not remote_jid.endswith("@g.us"):
            return
        is_ciphertext = web_message.get("messageStubType") == CIPHERTEXT_STUB
        has_stealth_meta = bool(web_message.get("stealthMeta"))
        if not is_ciphertext and not has_stealth_meta:
            return
        sender = key.get("participant")
        if not sender:
            return
        restrictions = read_group_restrictions()
        if not restrictions.get(remote_jid, {}).get("anti-payment"):
            return
        confidence = _confidence(web_message)
        if not confidence:
            return

        now = _now_ms()
        _sweep(now)
        tracker_key = f"{remote_jid}|{sender}"
        entry = _register_failure(tracker_key, now)
        if _on_cooldown(entry, now):
            return
        if await _sender_is_exempt(bridge, remote_jid, sender):
            return

        entry.last_alert_at = now
        tracker[tracker_key] = entry
        warning_log(
            "[stealth-payment] Suspeita "
            f"({confidence}) em {remote_jid} | autor {sender} | ocorrencias={entry.count}"
        )
        await apply_anti_payment_restriction(bridge, remote_jid, sender)
        number = _short_jid(sender)
        await bridge.send_message(
            remote_jid,
            {
                "text": (
                    "*Anti-Payment (Stealth)*\n"
                    f"Removi @{number}: tentou enviar uma cobranca oculta e indecifravel."
                ),
                "mentions": [sender],
            },
        )
    except Exception as error:
        error_log(f"[stealth-payment] Erro ao processar deteccao: {error}", error)

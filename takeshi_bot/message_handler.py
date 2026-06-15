from __future__ import annotations

from typing import Any

from takeshi_bot import config
from takeshi_bot.bridge import BaileysBridge
from takeshi_bot.context import CommandContext
from takeshi_bot.database import read_group_restrictions, read_restricted_message_types
from takeshi_bot.logger import error_log
from takeshi_bot.middlewares.permissions import is_admin
from takeshi_bot.messages import clear_chat
from takeshi_bot.utils import as_dict, as_str, get_nested_message
from takeshi_bot.utils.group_status_message import has_group_status_message
from takeshi_bot.utils.payment_message import has_payment_message


def has_direct_media(web_message: dict[str, Any], media_type: str) -> bool:
    return get_nested_message(web_message, media_type) is not None


async def apply_anti_payment_restriction(
    bridge: BaileysBridge, remote_jid: str, user_lid: str
) -> None:
    try:
        await bridge.group_setting_update(remote_jid, "announcement")
    except Exception as error:
        error_log("Erro ao fechar o grupo pelo anti-payment.", error)

    await bridge.group_participants_update(remote_jid, [user_lid], "remove")

    await bridge.send_message(
        remote_jid,
        {
            "text": (
                f"{config.BOT_EMOJI} Anti-payment ativado! "
                "Usuario removido por enviar cobranca."
            )
        },
    )
    await bridge.send_message(remote_jid, {"text": clear_chat()})
    try:
        await bridge.group_setting_update(remote_jid, "not_announcement")
    except Exception as error:
        error_log("Erro ao abrir o grupo pelo anti-payment.", error)


async def message_handler(bridge: BaileysBridge, web_message: dict[str, Any]) -> None:
    try:
        key = as_dict(web_message.get("key"))
        remote_jid = as_str(key.get("remoteJid"))
        if not remote_jid or not remote_jid.endswith("@g.us") or key.get("fromMe"):
            return
        user_lid = as_str(key.get("participant"))
        if not user_lid or user_lid in {config.OWNER_LID, config.BOT_LID}:
            return

        ctx = CommandContext.from_web_message(bridge, web_message)
        if ctx is None or await is_admin(ctx, user_lid):
            return

        restrictions = read_group_restrictions()
        group_restrictions = restrictions.get(remote_jid, {})

        if group_restrictions.get("anti-payment") and has_payment_message(web_message):
            await apply_anti_payment_restriction(bridge, remote_jid, user_lid)
            return

        if group_restrictions.get("anti-status-grupo") and has_group_status_message(
            web_message
        ):
            await bridge.group_participants_update(remote_jid, [user_lid], "remove")
            await bridge.delete_message(remote_jid, key)
            return

        restricted_types = read_restricted_message_types()
        for media_type in restricted_types.keys():
            if group_restrictions.get(f"anti-{media_type}") and has_direct_media(
                web_message, media_type
            ):
                await bridge.delete_message(
                    remote_jid,
                    {
                        "remoteJid": remote_jid,
                        "fromMe": key.get("fromMe", False),
                        "id": key.get("id"),
                        "participant": user_lid,
                    },
                )
                return
    except Exception as error:  # noqa: BLE001 - moderation boundary
        error_log(
            "Erro ao processar mensagem restrita. Verifique se eu estou como admin do grupo!",
            error,
        )

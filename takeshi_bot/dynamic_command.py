from __future__ import annotations

from takeshi_bot import config
from takeshi_bot.commands.registry import registry
from takeshi_bot.context import CommandContext
from takeshi_bot.database import (
    get_auto_responder_response,
    get_prefix,
    is_active_anti_link_group,
    is_active_auto_responder_group,
    is_active_auto_sticker_group,
    is_active_group,
    is_active_only_admins,
)
from takeshi_bot.errors import DangerError, InvalidParameterError, WarningError
from takeshi_bot.logger import error_log
from takeshi_bot.middlewares.permissions import (
    check_permission,
    has_type_and_command,
    is_admin,
    is_bot_owner,
    is_link,
    verify_prefix,
)
from takeshi_bot.services.sticker import create_sticker
from takeshi_bot.utils import as_dict


async def dynamic_command(ctx: CommandContext) -> None:
    match = registry.find(ctx.command_name)
    command_type = match.type
    command = match.command

    if config.ONLY_GROUP_ID and config.ONLY_GROUP_ID != ctx.remote_jid:
        return

    active_group = is_active_group(ctx.remote_jid)

    if (
        active_group
        and is_active_anti_link_group(ctx.remote_jid)
        and is_link(ctx.full_message)
        and ctx.user_lid
        and not await is_admin(ctx)
    ):
        await ctx.bridge.group_participants_update(
            ctx.remote_jid, [ctx.user_lid], "remove"
        )
        await ctx.send_reply("Anti-link ativado! Voce foi removido por enviar um link!")
        key = as_dict(ctx.web_message.get("key"))
        await ctx.bridge.delete_message(
            ctx.remote_jid,
            {
                "remoteJid": ctx.remote_jid,
                "fromMe": False,
                "id": key.get("id"),
                "participant": key.get("participant"),
            },
        )
        return

    if active_group and is_active_auto_sticker_group(ctx.remote_jid):
        if ctx.is_image or ctx.is_video:
            await create_sticker(ctx)
            return

    if active_group:
        if not verify_prefix(ctx.prefix, ctx.remote_jid) or not has_type_and_command(
            command_type, command
        ):
            if is_active_auto_responder_group(ctx.remote_jid):
                response = get_auto_responder_response(ctx.full_message)
                if response:
                    await ctx.send_reply(response)
                    return

            if "prefixo" in ctx.full_message.lower():
                await ctx.send_react(config.BOT_EMOJI)
                group_prefix = get_prefix(ctx.remote_jid)
                await ctx.send_reply(
                    f"O padrao e: {group_prefix}\n"
                    f"Use {group_prefix}menu para ver os comandos disponiveis!"
                )
            return

        if not await check_permission(command_type, ctx):
            await ctx.send_error_reply("Voce nao tem permissao para executar este comando!")
            return

        if is_active_only_admins(ctx.remote_jid) and not await is_admin(ctx):
            await ctx.send_warning_reply("Somente administradores podem executar comandos!")
            return

    if not is_bot_owner(ctx.user_lid) and not active_group:
        if verify_prefix(ctx.prefix, ctx.remote_jid) and has_type_and_command(
            command_type, command
        ):
            if command and command.name != "on":
                await ctx.send_warning_reply(
                    "Este grupo esta desativado! Peca para o dono do grupo ativar o bot!"
                )
                return
            if not await check_permission(command_type, ctx):
                await ctx.send_error_reply(
                    "Voce nao tem permissao para executar este comando!"
                )
                return
        else:
            return

    if not verify_prefix(ctx.prefix, ctx.remote_jid):
        return

    group_prefix = get_prefix(ctx.remote_jid)
    if ctx.full_message == group_prefix:
        await ctx.send_react(config.BOT_EMOJI)
        await ctx.send_reply(
            f"Este e meu prefixo! Use {group_prefix}menu para ver os comandos disponiveis!"
        )
        return

    if not has_type_and_command(command_type, command):
        await ctx.send_warning_reply(
            f"Comando nao encontrado! Use {group_prefix}menu para ver os comandos disponiveis!"
        )
        return

    assert command is not None
    ctx.type = command_type
    try:
        await command.handle(ctx)
    except InvalidParameterError as error:
        await ctx.send_warning_reply(f"Parametros invalidos! {error}")
    except WarningError as error:
        await ctx.send_warning_reply(str(error))
    except DangerError as error:
        await ctx.send_error_reply(str(error))
    except Exception as error:  # noqa: BLE001 - command boundary
        error_log(f"Erro ao executar comando {command.name}", error)
        await ctx.send_error_reply(
            f"Ocorreu um erro ao executar o comando {command.name}!\n\n"
            f"Detalhes: {error}"
        )

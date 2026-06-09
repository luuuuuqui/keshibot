from __future__ import annotations

import asyncio
import re

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.errors import DangerError

DANGEROUS_COMMANDS = [
    ":()",
    "mkfs",
    "fdisk",
    "parted",
    "format",
    "halt",
    "poweroff",
    "reboot",
    "shutdown",
    "init 0",
    "init 6",
]

DANGEROUS_PATTERNS = [
    re.compile(pattern, re.I)
    for pattern in [
        r":\(\)\s*\{",
        r"rm\s+-rf\s+\/($|\s)",
        r"rm\s+-rf\s+~\/\*",
        r"rm\s+-rf\s+\*($|\s)",
        r"dd\s+.*of=\/dev\/sd[a-z]",
        r"mkfs\.[a-z]+\s+\/dev",
        r":\(\)\s*\{.*fork",
        r"curl.*\|\s*bash",
        r"wget.*\|\s*bash",
        r"curl.*\|\s*sh",
        r"wget.*\|\s*sh",
        r"chmod\s+777\s+\/",
        r"chown\s+.*\s+\/",
        r">\s*\/dev\/sd[a-z]",
    ]
]


def _safety_reason(command: str) -> str | None:
    lower = command.strip().lower()
    for dangerous in DANGEROUS_COMMANDS:
        if dangerous.lower() in lower:
            return f"Comando perigoso detectado: {dangerous}"
    for pattern in DANGEROUS_PATTERNS:
        if pattern.search(command):
            return "Padrao perigoso detectado: operacao destrutiva bloqueada"
    return None


async def handle(ctx: CommandContext) -> None:
    command = ctx.full_args.strip()
    if not command:
        raise DangerError("Uso correto: /exec comando")
    reason = _safety_reason(command)
    if reason:
        raise DangerError(f"Comando bloqueado por seguranca!\n\nMotivo: {reason}")

    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    try:
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=15)
    except asyncio.TimeoutError as error:
        process.kill()
        await process.wait()
        raise DangerError("Comando cancelado por timeout (15s)") from error
    output = (stdout or stderr).decode("utf-8", errors="replace") or "Comando executado sem saida."
    if len(output) > 3500:
        output = output[:3500] + "\n\n... (saida truncada)"
    await ctx.send_success_reply(f"*Resultado:*\n\n```bash\n{output}\n```")


command = Command(
    name="exec",
    description="Executa comandos do terminal pelo bot.",
    commands=["exec"],
    usage="/exec comando",
    handle=handle,
)

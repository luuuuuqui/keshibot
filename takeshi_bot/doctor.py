from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

from takeshi_bot.commands.registry import registry
from takeshi_bot.paths import AUTH_DIR, BRIDGE_SCRIPT, DATABASE_DIR, TEMP_DIR, ensure_runtime_dirs


def _check_binary(name: str, args: list[str]) -> tuple[bool, str]:
    binary = shutil.which(name)
    if not binary:
        return False, f"{name} nao encontrado no PATH"
    try:
        result = subprocess.run(
            [binary, *args],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except Exception as error:  # noqa: BLE001 - diagnostic boundary
        return False, f"{name} falhou: {error}"
    output = (result.stdout or result.stderr).strip().splitlines()
    version = output[0] if output else binary
    return result.returncode == 0, version


def _command_mapping() -> tuple[bool, str]:
    js_commands = {
        path.relative_to("src/commands").with_suffix("").as_posix()
        for path in Path("src", "commands").rglob("*.js")
        if not path.name.startswith("\U0001f916")
    }
    py_modules = {
        path.relative_to("takeshi_bot/commands")
        .with_suffix("")
        .as_posix()
        .replace("_", "-")
        for path in Path("takeshi_bot", "commands").rglob("*.py")
        if path.name
        not in {"__init__.py", "base.py", "registry.py", "_helpers.py", "_restriction.py"}
    }
    missing = sorted(js_commands - py_modules)
    if missing:
        return False, f"faltando: {', '.join(missing[:10])}"
    return True, f"{len(py_modules)}/{len(js_commands)} comandos mapeados"


def run_doctor() -> int:
    ensure_runtime_dirs()
    checks: list[tuple[str, bool, str]] = []

    checks.append(("python", sys.version_info >= (3, 12), sys.version.split()[0]))
    checks.append(("node", *_check_binary("node", ["--version"])))
    checks.append(("ffmpeg", *_check_binary("ffmpeg", ["-version"])))
    checks.append(("bridge", BRIDGE_SCRIPT.exists(), str(BRIDGE_SCRIPT)))
    checks.append(("database-dir", DATABASE_DIR.exists(), str(DATABASE_DIR)))
    checks.append(("temp-dir", TEMP_DIR.exists(), str(TEMP_DIR)))
    checks.append(("auth-dir", AUTH_DIR.exists(), str(AUTH_DIR)))

    counts = {name: len(commands) for name, commands in registry.all_commands().items()}
    checks.append(("registry", sum(counts.values()) > 0, str(counts)))
    checks.append(("command-map", *_command_mapping()))

    width = max(len(name) for name, _, _ in checks)
    failed = False
    for name, ok, detail in checks:
        status = "OK" if ok else "FAIL"
        print(f"{name.ljust(width)}  {status}  {detail}")
        failed = failed or not ok
    return 1 if failed else 0


def main() -> None:
    raise SystemExit(run_doctor())


if __name__ == "__main__":
    main()

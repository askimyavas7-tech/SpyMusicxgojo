# Spy/core/git.py
# Heroku / Docker uyumlu güvenli sürüm
# VPS için yazılmış otomatik git update sistemi KALDIRILDI

import asyncio
import shlex
from typing import Tuple

from ..logging import LOGGER


def install_req(cmd: str) -> Tuple[str, str, int, int]:
    async def install_requirements():
        args = shlex.split(cmd)
        process = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        return (
            stdout.decode("utf-8", "replace").strip(),
            stderr.decode("utf-8", "replace").strip(),
            process.returncode,
            process.pid,
        )

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    return loop.run_until_complete(install_requirements())


def git():
    """
    Heroku container ortamında .git klasörü bulunmaz.
    Bu yüzden otomatik güncelleme sistemi tamamen devre dışı bırakıldı.
    Botun crash vermemesi için güvenli boş fonksiyon.
    """
    LOGGER(__name__).info("Git auto-update system disabled (Heroku compatible mode)")
    return

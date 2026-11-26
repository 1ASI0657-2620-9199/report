"""Capture real Windows CMD windows executing FinanZen commands.

Uses native CMD, a console framebuffer text read and a physical window screenshot.
No HTML, terminal emulation, image synthesis, overlays or reconstructed output.
"""
import argparse
import ctypes
from ctypes import wintypes
from datetime import datetime
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import time
from zoneinfo import ZoneInfo

from PIL import ImageGrab
import win32con
import win32api
import win32gui

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "evidencias/sprint-3/docker"
KERNEL = ctypes.WinDLL("kernel32", use_last_error=True)
USER = ctypes.WinDLL("user32", use_last_error=True)


class COORD(ctypes.Structure):
    _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]


class RECT(ctypes.Structure):
    _fields_ = [("Left", ctypes.c_short), ("Top", ctypes.c_short),
                ("Right", ctypes.c_short), ("Bottom", ctypes.c_short)]


class BUFFER_INFO(ctypes.Structure):
    _fields_ = [("size", COORD), ("cursor", COORD), ("attributes", wintypes.WORD),
                ("window", RECT), ("maximum_size", COORD)]


class FONT_INFO(ctypes.Structure):
    _fields_ = [("cbSize", wintypes.ULONG), ("nFont", wintypes.DWORD), ("size", COORD),
                ("family", wintypes.UINT), ("weight", wintypes.UINT),
                ("face", wintypes.WCHAR * 32)]


def window_named(title):
    found = []
    def visit(hwnd, _):
        if win32gui.IsWindowVisible(hwnd) and title in win32gui.GetWindowText(hwnd):
            found.append(hwnd)
    win32gui.EnumWindows(visit, None)
    return found[0] if found else None


def console_text(process_id):
    """Read the target CMD's actual screen buffer, not a separately rerun command."""
    KERNEL.FreeConsole()
    if not KERNEL.AttachConsole(process_id):
        raise ctypes.WinError(ctypes.get_last_error())
    KERNEL.CreateFileW.restype = wintypes.HANDLE
    handle = KERNEL.CreateFileW("CONOUT$", 0x80000000 | 0x40000000, 3, None, 3, 0, None)
    if handle == wintypes.HANDLE(-1).value:
        raise ctypes.WinError(ctypes.get_last_error())
    try:
        font = FONT_INFO()
        font.cbSize = ctypes.sizeof(font)
        font.size = COORD(0, 18)
        font.family = 54
        font.weight = 400
        font.face = "Consolas"
        KERNEL.SetCurrentConsoleFontEx(wintypes.HANDLE(handle), False, ctypes.byref(font))
        info = BUFFER_INFO()
        if not KERNEL.GetConsoleScreenBufferInfo(wintypes.HANDLE(handle), ctypes.byref(info)):
            raise ctypes.WinError(ctypes.get_last_error())
        count = info.size.X * info.size.Y
        buffer = ctypes.create_unicode_buffer(count + 1)
        read = wintypes.DWORD()
        if not KERNEL.ReadConsoleOutputCharacterW(wintypes.HANDLE(handle), buffer, count, COORD(0, 0), ctypes.byref(read)):
            raise ctypes.WinError(ctypes.get_last_error())
        data = buffer[:read.value]
        return "\n".join(data[i:i + info.size.X].rstrip() for i in range(0, len(data), info.size.X)).strip()
    finally:
        KERNEL.CloseHandle(wintypes.HANDLE(handle))
        KERNEL.FreeConsole()


CASES = {
    "01-desarrollo-commits": [
        "git remote get-url origin",
        "git log -1 --oneline -- Dockerfile compose.yaml",
        'git log -1 --date=short --format="%%h %%ad %%an" -- Dockerfile compose.yaml',
        "git ls-files Dockerfile compose.yaml requirements-kafka.txt",
        "docker compose config --services",
        'git -C ..\\front log -1 --format="%%h %%s" -- Dockerfile nginx.conf',
    ],
    "02-dockerfile": ["type Dockerfile"],
    "03-compose-configuracion": [
        "docker compose config --quiet",
        "docker compose config --services",
        "docker compose config --volumes",
        "docker compose config --images",
    ],
    "04-contenedores-activos": [
        "docker compose version",
        'docker version --format "Engine {{.Server.Version}} - Client {{.Client.Version}}"',
        'docker compose ps --all --format "table {{.Name}}\\t{{.State}}\\t{{.Status}}\\t{{.Ports}}"',
    ],
    "05-ejecucion-integrada": [".\\.venv\\Scripts\\python.exe scripts\\verify_docker.py"],
    "06-health-checks": ["python ..\\report\\scripts\\verificar_health_docker.py"],
    "07-logs-servicios": ["docker compose logs --no-color --tail 6 financial-records budget-service notification-service device-service"],
    "08-kafka-topics-consumidor": [
        "docker compose exec -T kafka /opt/kafka/bin/kafka-topics.sh --bootstrap-server kafka:19092 --list",
    ],
    "09-compose-despliegue": [
        "docker compose --progress quiet up -d --wait --wait-timeout 240",
        'docker compose ps --format "table {{.Service}}\\t{{.State}}\\t{{.Status}}"',
    ],
}


def capture(case, backend, keep_open=False):
    OUTPUT.mkdir(parents=True, exist_ok=True)
    controls = OUTPUT / "_capture"
    controls.mkdir(exist_ok=True)
    done = controls / (case + ".done")
    results = controls / (case + ".codes")
    if done.exists():
        done.unlink()
    if results.exists():
        results.unlink()
    title = "FinanZen - CMD - " + case
    lines = ["@echo off", "chcp 65001 >nul", "title " + title, "mode con cols=142 lines=46",
             'cd /d "' + str(backend) + '"', "prompt FinanZen$G", "@echo on", "cd", "@echo off"]
    for index, command in enumerate(CASES[case]):
        lines.extend(["@echo on", command, "@echo off", f'>>"{results}" echo {index}:%errorlevel%'])
    lines.extend([f'>"{done}" echo finished', "@echo on"])
    batch = controls / (case + ".cmd")
    batch.write_bytes(("\r\n".join(lines) + "\r\n").encode("utf-8"))
    process = subprocess.Popen([os.environ.get("COMSPEC", "cmd.exe"), "/d", "/k", str(batch)],
                               cwd=backend, creationflags=subprocess.CREATE_NEW_CONSOLE)
    try:
        deadline = time.monotonic() + 180
        while not done.exists() or not window_named(title):
            if process.poll() is not None:
                raise RuntimeError("CMD exited before completing the capture")
            if time.monotonic() > deadline:
                raise TimeoutError("CMD capture timed out")
            time.sleep(0.2)
        time.sleep(0.6)
        console_text(process.pid)
        hwnd = window_named(title)
        if not hwnd:
            raise RuntimeError("No visible CMD window found")
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 50, 55, 1500, 940, win32con.SWP_SHOWWINDOW)
        try:
            win32gui.SetForegroundWindow(hwnd)
        except Exception:
            pass
        if win32gui.GetForegroundWindow() == hwnd:
            for _ in range(4):
                win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
                try:
                    win32api.keybd_event(0xBB, 0, 0, 0)
                finally:
                    win32api.keybd_event(0xBB, 0, win32con.KEYEVENTF_KEYUP, 0)
                    win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
                time.sleep(0.12)
        time.sleep(0.7)
        text = console_text(process.pid)
        rectangle = win32gui.GetWindowRect(hwnd)
        image = ImageGrab.grab(bbox=rectangle, all_screens=True)
        image_path = OUTPUT / (case + ".png")
        image.save(image_path)
        win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                              win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        (OUTPUT / (case + ".txt")).write_text(text + "\n", encoding="utf-8")
        codes = [int(row.split(":")[1]) for row in results.read_text().splitlines()]
        entry = {
            "case": case, "captured_at": datetime.now(ZoneInfo("America/Lima")).isoformat(),
            "application": "cmd.exe", "window_title": win32gui.GetWindowText(hwnd),
            "window_class": win32gui.GetClassName(hwnd), "process_id": process.pid,
            "method": "PIL.ImageGrab of the visible native CMD window; text read from its console buffer",
            "rectangle": rectangle, "image_size": image.size,
            "commands": CASES[case], "exit_codes": codes,
            "image": image_path.name, "sha256": sha256(image_path.read_bytes()).hexdigest(),
            "transcript": case + ".txt", "image_edited": False, "ai_image_generation": False,
        }
        (OUTPUT / (case + ".json")).write_text(json.dumps(entry, ensure_ascii=False, indent=2), encoding="utf-8")
        if any(codes):
            raise RuntimeError("A command failed; inspect the actual CMD screenshot: " + case)
        print(json.dumps(entry, ensure_ascii=False), flush=True)
    finally:
        if not keep_open and process.poll() is None:
            process.terminate()
            process.wait(timeout=5)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--backend", type=Path, default=ROOT.parent / "back")
    parser.add_argument("--case", choices=list(CASES))
    parser.add_argument("--keep-open", action="store_true")
    args = parser.parse_args()
    backend = args.backend.resolve()
    if not (backend / "compose.yaml").is_file():
        raise SystemExit("Expected the FinanZen back checkout with compose.yaml.")
    for name in ([args.case] if args.case else CASES):
        capture(name, backend, args.keep_open)

import ctypes
import time
import psutil
import sys
import os

targets = ["GTA5_Enhanced.exe", "GTA5.exe"]
found_procs = [p for p in psutil.process_iter(['pid', 'name']) if p.info['name'] in targets]

if not found_procs:
    print("Процессы не найдены. Выход через 3 секунды...")
    time.sleep(3)
    sys.exit()

def suspend_resume(proc, action):
    PROCESS_SUSPEND_RESUME = 0x0800
    handle = ctypes.windll.kernel32.OpenProcess(PROCESS_SUSPEND_RESUME, False, proc.pid)
    if not handle:
        print(f"❌ Не удалось получить доступ к процессу: {proc.pid}")
        return
    NtSuspendProcess = ctypes.windll.ntdll.NtSuspendProcess
    NtResumeProcess = ctypes.windll.ntdll.NtResumeProcess
    if action == "suspend":
        NtSuspendProcess(handle)
        print(f"⏸ Приостановлен: {proc.name()}")
    elif action == "resume":
        NtResumeProcess(handle)
        print(f"▶ Возобновлён: {proc.name()}")
    ctypes.windll.kernel32.CloseHandle(handle)

# Приостановка
for proc in found_procs:
    suspend_resume(proc, "suspend")

print("⌛ Приостановка на 10 секунд...")
time.sleep(10)

# Возобновление
for proc in found_procs:
    suspend_resume(proc, "resume")

print("\n✅ Все процессы восстановлены. Закрытие через 5 секунд...")
time.sleep(5)

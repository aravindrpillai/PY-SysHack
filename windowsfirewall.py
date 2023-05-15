import ctypes
from ctypes import wintypes

class ShellExecuteInfo(ctypes.Structure):
    _fields_ = [
        ('cbSize', wintypes.DWORD),
        ('fMask', wintypes.ULONG),
        ('hwnd', wintypes.HWND),
        ('lpVerb', ctypes.c_char_p),
        ('lpFile', ctypes.c_char_p),
        ('lpParameters', ctypes.c_char_p),
        ('lpDirectory', ctypes.c_char_p),
        ('nShow', wintypes.INT),
        ('hInstApp', wintypes.HINSTANCE),
        ('lpIDList', wintypes.LPVOID),
        ('lpClass', ctypes.c_char_p),
        ('hKeyClass', wintypes.HKEY),
        ('dwHotKey', wintypes.DWORD),
        ('hIcon', wintypes.HANDLE),
        ('hProcess', wintypes.HANDLE),
    ]

command  = 'netsh advfirewall set allprofiles state off'
sei = ShellExecuteInfo()
sei.cbSize = ctypes.sizeof(sei)
sei.fMask = 0x0000000C
sei.lpVerb = b'runas'
sei.lpFile = b'C:\\Windows\\System32\\cmd.exe'
sei.lpParameters = command.encode('utf-8')
sei.nShow = 1
ret = ctypes.windll.shell32.ShellExecuteExW(ctypes.byref(sei))
if ret != 0:
    # Wait for the process to finish before returning
    ctypes.windll.kernel32.WaitForSingleObject(sei.hProcess, -1)
    ctypes.windll.kernel32.CloseHandle(sei.hProcess)
    print("success")
else:
    print("failed")
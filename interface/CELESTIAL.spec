# CELESTIAL.spec — Build script for PyInstaller
# Place this in: C:\Users\Chuck\Desktop\AXISABLE_CELESTIAL_USB_BOOT\

# -*- mode: python -*-
from PyInstaller.utils.hooks import collect_data_files
import glob

block_cipher = None

# Gather agent folders and their contents
agent_data = [(f, f) for f in glob.glob("agents/*/*.json")]
agent_data += [(f, f) for f in glob.glob("agents/*/voice.vpk")]

a = Analysis(
    ['interface/interface_celestial_unified.py'],
    pathex=[],
    binaries=[],
    datas=[
        *agent_data,
        ('assets/icon.png', 'assets'),
        ('assets/tray_icon.png', 'assets'),
        ('assets/icon.ico', 'assets'),
        ('core/voice_engine.py', 'core'),
        ('core/memory_keeper.py', 'core'),
        ('core/agent_manager.py', 'core'),
        ('core/child_mode.py', 'core'),
    ],
    hiddenimports=[
        'PyQt5.QtWidgets',
        'PyQt5.QtGui',
        'PyQt5.QtCore',
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=False,
    name='CELESTIAL',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon='assets/icon.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='CELESTIAL'
)

# CELESTIAL.spec
# -*- mode: python -*-
from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

a = Analysis(
    ['interface/interface_celestial_unified.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets/icon.ico', 'assets'),
        ('assets/icon.png', 'assets'),
        ('assets/tray_icon.png', 'assets'),
        ('assets/spinner/*.png', 'assets/spinner'),
        ('offline_packages/requirements.txt', 'offline_packages'),
        *collect_data_files('core'),
        *collect_data_files('agents'),
        *collect_data_files('curriculum'),
        *collect_data_files('docs')
    ],
    hiddenimports=['PyQt5.sip', 'PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets'],
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
    a.binaries,
    a.zipfiles,
    a.datas,
    name='CELESTIAL',
    debug=False,
    strip=False,
    upx=True,
    console=False,
    icon='assets/icon.ico'
)

)


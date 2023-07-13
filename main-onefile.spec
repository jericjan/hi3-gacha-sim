# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

from pathlib import Path

current_dir = Path.cwd()
venv = current_dir / r"venv\Lib\site-packages"

a = Analysis(['src\\main.py'],
             pathex=[str(venv), str(current_dir)],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='HI3_Gacha_Sim',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )

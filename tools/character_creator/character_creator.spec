# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['-m', 'tools.character_creator'],
             pathex=[],
             binaries=[],
             datas=[('tools/character_creator/srd_data.py','tools/character_creator')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[])
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='character_creator',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='character_creator')

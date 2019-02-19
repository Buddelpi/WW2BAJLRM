# -*- mode: python -*-
from kivy.deps import sdl2, glew

block_cipher = None

added_files = [
         ( 'C:\Users\Ercsi\Documents\GitHub\WW2BAJLRM\Images', 'Images' ),
         ( 'C:\Users\Ercsi\Documents\GitHub\WW2BAJLRM\Sounds', 'Sounds' ),
         ( 'C:\Users\Ercsi\Documents\GitHub\WW2BAJLRM\missionnaire.kv', '.' ),
         ( 'C:\Users\Ercsi\Documents\GitHub\WW2BAJLRM\questions.json', '.' )
         ]

a = Analysis(['C:\\Users\\Ercsi\\Documents\\GitHub\\WW2BAJLRM\\main.py'],
             pathex=['C:\\Users\\Ercsi\\Documents\\GitHub\\WW2BAJLRM'],
             binaries=[],
             datas=added_files,
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
          [],
          exclude_binaries=True,
          name='WW2BAMBSE',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
          

          
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               name='WW2BAMBSE')

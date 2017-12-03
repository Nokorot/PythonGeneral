# -*- mode: python -*-

block_cipher = None

def addResorces(a, data):
        for e in data:
                a.datas += [(e+'.png','/home/nokorot/uio/Documents/Python/snake/'+e+'.png','DATA')]

a = Analysis(['main.py'],
             pathex=['/home/nokorot/uio/Documents/Python/snake'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

addResorces(a, ['snake_head', 'snake_strait', 'snake_tail', 'snake_turn'])

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='main',
          debug=False,
          strip=False,
          upx=True,
          console=True )

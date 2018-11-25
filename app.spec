# -*- mode: python -*-

block_cipher = None


a = Analysis(['app.py'],
             pathex=['C:\\Users\\Nejc\\Projects\\Projekti 2016\\Career Night App'],
             binaries=[],
             datas=[('Data/icon.png','DATA'),('Data/startpage_background.png','DATA'),('Data/logo.png','DATA')],
             hiddenimports=['six'],
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
          name='CareerNight_app',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False,
		  icon = 'Data\icon.ico')

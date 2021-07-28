# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

def get_resources():
    data_files = []
    for file_name in os.listdir('assets'):
        data_files.append((os.path.join('assets', file_name), 'assets'))
    return data_files

a = Analysis(['main.py'],
             pathex=['C:\\Users\\Sebastien\\PycharmProjects\\Journaling'],
             binaries=[],
             datas=get_resources(),
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
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
          name='journaler',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None , icon='icon.ico')

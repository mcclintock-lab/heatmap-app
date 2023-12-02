# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['heatmapp.py'],
    pathex=['./.venv/lib/python3.11/site-packages'],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='heatmapp',
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
    icon=['heatmap-icon.png'],
)
app = BUNDLE(
    exe,
    name='heatmapp.app',
    icon='heatmap-icon.png',
    bundle_identifier=None,
)

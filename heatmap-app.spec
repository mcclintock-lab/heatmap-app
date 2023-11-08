# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['heatmap-app.py'],
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
    [],
    exclude_binaries=True,
    name='heatmap-app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['heatmap-icon.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='heatmap-app',
)
app = BUNDLE(
    coll,
    name='heatmap-app.app',
    icon='heatmap-icon.ico',
    bundle_identifier=None,
)

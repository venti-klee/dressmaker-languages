"""Build allowlisted source / Mac release archives, never bundling personal runtime data."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import zipfile

ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIRS = {'assistant', 'src', 'tests', 'docs', 'scripts', '.github'}
SOURCE_NAMES = {'LICENSE', 'VERSION', '.gitignore', '.gitattributes', 'Start.command', '启动翻译助手.command', '使用说明.md'}
SOURCE_SUFFIXES = {'.py', '.cs', '.html', '.json', '.md', '.yml', '.yaml'}
BINARY_NAMES = {
    'BepInEx/plugins/DressmakerLanguages/DressmakerLanguages.dll',
    '针影裁梦多语言助手.app/Contents/Info.plist',
    '针影裁梦多语言助手.app/Contents/MacOS/launch',
}


def selected_source_files():
    result = []
    for path in ROOT.rglob('*'):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if '__pycache__' in rel.parts or path.name == '.DS_Store':
            continue
        if len(rel.parts) == 1 and (path.name in SOURCE_NAMES or path.name.startswith('README') and path.suffix == '.md'):
            result.append(path)
        elif rel.parts[0] in SOURCE_DIRS and path.suffix in SOURCE_SUFFIXES:
            result.append(path)
    return sorted(result)


def manifest(files, version, kind):
    return {
        'version': version, 'archive_kind': kind,
        'files': [{'path': str(p.relative_to(ROOT)), 'bytes': p.stat().st_size,
                   'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in files],
        'excluded': ['data/', '.venv/', 'models/', 'work/', '.git/', 'game assets',
                     'official localization tables', 'personal settings, paths, logs and session tokens'],
        'manifest_note': 'UPLOAD-MANIFEST.json is generated at archive creation and is not self-hashed.',
    }


def create_archive(destination, files, version, kind):
    with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, 'Dressmaker-Languages/' + str(path.relative_to(ROOT)))
        archive.writestr('Dressmaker-Languages/UPLOAD-MANIFEST.json',
                         json.dumps(manifest(files, version, kind), ensure_ascii=False, indent=2) + '\n')
    with zipfile.ZipFile(destination) as archive:
        if archive.testzip() is not None:
            raise RuntimeError('Archive integrity check failed')
    print(destination.name + ': ' + str(len(files) + 1) + ' files')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=ROOT / 'dist')
    parser.add_argument('--source-only', action='store_true')
    args = parser.parse_args()
    version = (ROOT / 'VERSION').read_text().strip()
    if not re.fullmatch(r'\d+\.\d+\.\d+', version):
        raise ValueError('Invalid VERSION')
    args.out.mkdir(parents=True, exist_ok=True)
    files = selected_source_files()
    create_archive(args.out / ('Dressmaker-Languages-GitHub-' + version + '.zip'), files, version, 'source')
    if not args.source_only:
        binaries = [ROOT / name for name in sorted(BINARY_NAMES)]
        if any(not path.is_file() for path in binaries):
            raise RuntimeError('Compile the plugin and provide the Mac launcher before packaging a Mac release; or use --source-only.')
        create_archive(args.out / ('Dressmaker-Languages-Mac-' + version + '.zip'), files + binaries, version, 'mac-release')


if __name__ == '__main__':
    main()

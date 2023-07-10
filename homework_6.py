import re
import sys
from pathlib import Path
import shutil
current_path = Path('.')

CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")
TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()

JPEG_IMAGES = []
JPG_IMAGES = []
PNG_IMAGES = []
SVG_IMAGES = []

AVI_VIDEO = []
MP4_VIDEO = []
MOV_VIDEO = []
MKV_VIDEO = []

DOC_DOCUMENTS = []
DOCX_DOCUMENTS = []
TXT_DOCUMENTS = []
PDF_DOCUMENTS = []
XLSX_DOCUMENTS = []
PPTX_DOCUMENTS = []

MP3_AUDIO = []
OGG_AUDIO = []
WAV_AUDIO = []
AMR_AUDIO = []

ZIP_ARCHIVES = []
GZ_ARCHIVES = []
TAR_ARCHIVES = []

MY_OTHER = []

FOLDERS = []
EXTENSION = set()
UNKNOWN = set()

REGISTER_EXTENSION = {
    'JPEG': JPEG_IMAGES,'JPG': JPG_IMAGES,'PNG': PNG_IMAGES,'SVG': SVG_IMAGES,
    'MP3': MP3_AUDIO,'OGG': OGG_AUDIO,'WAV': WAV_AUDIO,'AMR': AMR_AUDIO,
    'AVI': AVI_VIDEO,'MP4': MP4_VIDEO,'MOV': MOV_VIDEO,'MKV': MKV_VIDEO,
    'DOC': DOC_DOCUMENTS,'DOCX': DOCX_DOCUMENTS,'TXT': TXT_DOCUMENTS,'PDF': PDF_DOCUMENTS,'XLSX': XLSX_DOCUMENTS,'PPTX': PPTX_DOCUMENTS,
    'ZIP': ZIP_ARCHIVES,'GZ': GZ_ARCHIVES,'TAR': TAR_ARCHIVES,
}

def normalize(name: str) -> str:
    t_name = name.translate(TRANS)
    t_name = re.sub(r'[^a-zA-Z0-9.]', '_', t_name)
    return t_name

def get_extension(filename: str) -> str:
    return Path(filename).suffix[1:].upper()

def scan(folder: Path) -> None:
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'MY_OTHER'):
                FOLDERS.append(item)
                scan(item)
            continue 

        ext = get_extension(item.name)  
        fullname = folder / item.name 
        if not ext:  
            MY_OTHER.append(fullname)
        else:
            try:
                container = REGISTER_EXTENSION[ext]
                EXTENSION.add(ext)
                container.append(fullname)
            except KeyError:
                UNKNOWN.add(ext)
                MY_OTHER.append(fullname)

def handle_pictures(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))

def handle_media(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))

def handle_audio(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))

def handle_documents(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))

def handle_other(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / filename.name)

def handle_archive(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    folder_for_file = target_folder / normalize(filename.name.replace(filename.suffix, ''))
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(filename, folder_for_file) 
    except shutil.ReadError:
        print('It is not archive')
        folder_for_file.rmdir()
    filename.unlink()

def handle_folder(folder: Path):
     try:
         folder.rmdir()
     except OSError:
         print(f"Can't delete folder: {folder}")

def main(folder: Path):
    scan(folder)
    for file in JPEG_IMAGES:
        handle_pictures(file, folder / 'images' / 'JPEG')
    for file in JPG_IMAGES:
        handle_pictures(file, folder / 'images' / 'JPG')
    for file in PNG_IMAGES:
        handle_pictures(file, folder / 'images' / 'PNG')
    for file in SVG_IMAGES:
        handle_pictures(file, folder / 'images' / 'SVG')

    for file in MP3_AUDIO:
        handle_audio(file, folder / 'audio' / 'MP3')
    for file in OGG_AUDIO:
        handle_audio(file, folder / 'audio' / 'OGG')
    for file in WAV_AUDIO:
        handle_audio(file, folder / 'audio' / 'WAV')
    for file in AMR_AUDIO:
        handle_audio(file, folder / 'audio' / 'AMR')


    for file in AVI_VIDEO:
        handle_media(file, folder / 'video' / 'AVI')
    for file in MP4_VIDEO:
        handle_media(file, folder / 'video' / 'MP4')
    for file in MOV_VIDEO:
        handle_media(file, folder / 'video' / 'MOV')
    for file in MKV_VIDEO:
        handle_media(file, folder / 'video' / 'MKV')

    for file in DOC_DOCUMENTS:
        handle_documents(file, folder / 'documents' / 'DOC')
    for file in DOCX_DOCUMENTS:
        handle_documents(file, folder / 'documents' / 'DOCX')
    for file in TXT_DOCUMENTS:
        handle_documents(file, folder / 'documents' / 'TXT')
    for file in PDF_DOCUMENTS:
        handle_documents(file, folder / 'documents' / 'PDF') 
    for file in XLSX_DOCUMENTS:
        handle_documents(file, folder / 'documents' / 'XLSX')
    for file in PPTX_DOCUMENTS:
        handle_documents(file, folder / 'documents' / 'PPTX') 


    for file in MY_OTHER:
        handle_other(file, folder / 'MY_OTHER')

    for file in ZIP_ARCHIVES:
        handle_archive(file, folder / 'archives' / 'ZIP')
    for file in GZ_ARCHIVES:
        handle_archive(file, folder / 'archives' / 'GZ')
    for file in TAR_ARCHIVES:
        handle_archive(file, folder / 'archives' / 'TAR')

    for folder in FOLDERS[::-1]:
         handle_folder(folder)

if __name__ == "__main__":
    if sys.argv[1]:
        folder_for_scan = Path(sys.argv[1])
        print(f'Start in folder: {folder_for_scan.resolve()}')
        main(folder_for_scan.resolve())

print(f'Images:{JPEG_IMAGES},{JPG_IMAGES},{PNG_IMAGES},{SVG_IMAGES}')
print(f'Video: {AVI_VIDEO},{MP4_VIDEO},{MOV_VIDEO},{MKV_VIDEO}')
print(f'Audio: {MP3_AUDIO}{OGG_AUDIO}{WAV_AUDIO}{AMR_AUDIO}')
print(f'Archives: {ZIP_ARCHIVES}{GZ_ARCHIVES}{TAR_ARCHIVES}')
print(f'Documents: {DOC_DOCUMENTS}{DOCX_DOCUMENTS}{TXT_DOCUMENTS}{PDF_DOCUMENTS}{XLSX_DOCUMENTS}{PPTX_DOCUMENTS}')
print(f'Archives: {MY_OTHER}')
print(f'Types of files in folder: {EXTENSION}')
print(f'Unknown files of types: {UNKNOWN}')
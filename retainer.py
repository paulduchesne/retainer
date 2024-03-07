
# simple script to backup files from source to destination location.

import hashlib
import pandas
import pathlib
import shutil
import tqdm

def checksum(filepath):

    ''' Standard MD5 hashing. '''

    with open(filepath, 'rb') as item:
        hash = hashlib.md5()
        for buff in iter(lambda: item.read(65536), b''):
            hash.update(buff)
        md5 = hash.hexdigest().lower()
        return md5

source_dir = pathlib.Path.home() / 'hold'
result_dir = pathlib.Path('/media/paulduchesne/VERT')

df = pandas.DataFrame(columns=['path', 'hash'])
source_files = sorted([x for x in source_dir.rglob('*') if x.is_file()])
print('hashing files.')
for file_path in tqdm.tqdm(source_files):
    file_hash = checksum(file_path)
    df.loc[len(df)] = [(file_path), (file_hash)]

# save df somewhere

print('copying files.')
for x in tqdm.tqdm(df.to_dict('records')):
    file_path, file_hash = x['path'], x['hash']
    result_path = result_dir / 'objects' / file_hash[:2] / f'{file_hash}{file_path.suffix}'
    if not result_path.exists():
        result_path.parents[0].mkdir(exist_ok=True)
        shutil.copyfile(file_path, result_path)

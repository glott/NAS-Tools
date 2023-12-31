###########################################################################
####################### CRC PROFILE BACKUP/UPDATER ########################
###########################################################################

########################### MODIFY THESE VALUES ###########################

# Directory where CRC Profiles and PrefSets will be backed up
# %CRC% will be replaced with the default CRC installation folder
# Do not delete the R before the quotes
BACKUP_DIR = R'%CRC%\Backups' 

# If 'True', files in your CRC folder will be replaced with updated files
# Set this to either 'True' or 'False' (without quotes)
RUN_UPDATE = True                                   

# This is the directory of the update files
# The UPDATE_DIR must have the same folder structure as CRC
# e.g. Profiles, PrefSets/STARS
UPDATE_DIR = R'C:\Users\Josh\Dropbox\VATSIM\CRC'

############################ DO NOT EDIT BELOW ############################

import os, shutil, zipfile, datetime

CRC_PATH = os.getenv('LOCALAPPDATA') + '\\CRC'
BACKUP_DIR = BACKUP_DIR.replace('%CRC%', CRC_PATH)

if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

def backup_files(main_dir, sub_dirs):
    output_zip = 'CRC Backup ' + datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S') + '.zip'
    output_zip = os.path.join(BACKUP_DIR, output_zip)

    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root_dir in sub_dirs:
            root_dir = os.path.join(main_dir, root_dir)
            for root, _, files in os.walk(root_dir):
                for file in files:
                    if not file.endswith('.lnk'):
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, os.path.relpath(file_path, main_dir))

    print(f'Created \'{os.path.basename(output_zip)}\'')

def copy_files(source_dir, dest_dir, sub_dirs):
    prev_header = ''
    for dir_ in sub_dirs:
        root_dir = os.path.join(source_dir, dir_)
        for root, _, files in os.walk(root_dir):
            for file in files:
                if file.endswith('.json') and 'Backup' not in root:
                    file_path = os.path.join(root, file)
                    header = os.sep.join(os.path.relpath(file_path, source_dir).split(os.sep)[:-1])
                    if prev_header != header:
                        prev_header = header
                        print('\nUpdated \'' + header.replace(os.sep, '/') + '\'')

                    dest_path = os.path.join(dest_dir, header.replace('/', os.sep))
                    shutil.copy(file_path, dest_path)
                    print('    ' + file.split('.')[0])

print('=============================================')        
print('======== CRC PROFILE BACKUP/UPDATER =========')
print('=============================================')

print(f'\nBACKUP_DIR = ' + BACKUP_DIR.replace(os.getenv('LOCALAPPDATA'), '%LOCALAPPDATA%'))
print(f'RUN_UPDATE = {RUN_UPDATE}')
print(f'UPDATE_DIR = {UPDATE_DIR}')
print('\n=============================================\n')

backup_files(CRC_PATH, ['Profiles', 'PrefSets'])

if RUN_UPDATE and os.path.exists(UPDATE_DIR):
    copy_files(UPDATE_DIR, CRC_PATH, ['Profiles', 'PrefSets'])

input('\nPress enter to close...')
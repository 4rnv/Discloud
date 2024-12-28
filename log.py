import      json
import      hashlib
from        os          import      listdir
from        os.path     import      isfile, join, getsize, exists

class File:
    def __init__(self,name,hash,size):
        self.name = name
        self.hash = hash
        self.size = size

    def calculate_file_size(file_path):
        return getsize(file_path)

    def get_file_hash(file_path, algorithm='sha256'):
        hash_func = hashlib.new(algorithm)
        with open(file_path, 'rb') as file:
            while chunk := file.read(8192):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    
def load_logged_files() -> list:
    if not exists('db.json'):
        with open('db.json', 'w') as db:
            json.dump([], db)
    try:
        with open('db.json', 'r') as db:
            return json.load(db)
    except:
        return []

def save_data_to_json(db_file, data):
    with open(db_file, 'w') as f:
        json.dump(data, f, indent=4)

folder_path = r'upload'
files = [f'{folder_path}/{f}' for f in listdir(folder_path) if isfile(join(folder_path, f))]
logged_files = load_logged_files()
existing_file_hashes = {file_info['hash'] for file_info in logged_files}

def log_file_info(files, existing_file_hashes):
    print(files)
    print(existing_file_hashes)

    for file in files:
        file_hash = File.get_file_hash(file)
        file_size = File.calculate_file_size(file)
        file_obj = File(file, file_hash, file_size)

        file_data = {
            'name': file_obj.name,
            'hash': file_obj.hash,
            'size': file_obj.size
        }

        if file_obj.hash not in existing_file_hashes:
            logged_files.append(file_data)
            existing_file_hashes.add(file_obj.hash)

    save_data_to_json('db.json', logged_files)
    print(logged_files)
    return logged_files
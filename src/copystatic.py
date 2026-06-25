import os
import shutil
def source_to_destination(src_path: str, dst_path: str):
    if not os.path.exists(dst_path):
        os.mkdir(dst_path)
    
    folder = os.listdir(src_path)
    for filename in folder:
        from_path = os.path.join(src_path, filename)
        to_path = os.path.join(dst_path, filename)
        if os.path.isfile(from_path):
            shutil.copy(from_path, to_path)
        else:
            source_to_destination(from_path, to_path)

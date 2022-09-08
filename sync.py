import hashlib
import os
import shutil
from pathlib import Path
import sys

def hashfile(file):
  
  # A arbitrary (but fixed) buffer
  # size (change accordingly)
  # 65536 = 65536 bytes = 64 kilobytes
  BUF_SIZE = 65536

  # Initializing the sha256() method
  sha256 = hashlib.sha256()

  # Opening the file provided as
  # the first commandline argument
  with open(file, 'rb') as f:
    while True:
        # reading data = BUF_SIZE from
        # the file and saving it in a
        # variable
        data = f.read(BUF_SIZE)

        # True if eof = 1
        if not data:
            break
  
        # Passing that data to that sh256 hash
        # function (updating the function with
        # that data)
        sha256.update(data)
  
      
    # sha256.hexdigest() hashes all the input
    # data passed to the sha256() via sha256.update()
    # Acts as a finalize method, after which
    # all the input data gets hashed hexdigest()
    # hashes the data, and returns the output
    # in hexadecimal format
    return sha256.hexdigest()

def sync(source, dest):
  source_files = os.listdir(source)
  dest_files = os.listdir(dest)
  hashed_source_files = {}
  hashed_dest_files = {}
  for s in source_files:
    hashed_source_files[s] = hashfile(os.path.join(source, s))
  for d in dest_files:
    hashed_dest_files[d] = hashfile(os.path.join(dest, d))

  
  for x, y in hashed_source_files.items(): 
    # If a file exists in the source but not in the destination, copy the file over.
    if y not in hashed_dest_files.values():
      shutil.copy2(os.path.join(source, x), dest)
      
    # If a file exists in the source, but it has a different name than in the destination, rename the destination file to match.
    if y in hashed_dest_files.values():
      key = [k for k, v in hashed_dest_files.items() if v == y][0]
      print(key)
      os.rename(os.path.join(dest, key), os.path.join(dest, x))
      
  # If a file exists in the destination but not in the source, remove it.    
  for x, y in hashed_dest_files.items():
    if y not in hashed_source_files.values():
      os.remove(os.path.join(dest, x))

  pass

sync(sys.argv[1], sys.argv[2])
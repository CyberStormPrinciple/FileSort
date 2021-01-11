# Desc: Program that sorts contents of directories into folders based on a filter file.
# Author: Nathan Gilbert
import shutil, os, sys


def get_file_type(file_name):
  print(file_name)
  type = file_name.split('.')
  if len(type) < 2:
    pass
  else:
    return file_name.split('.')[1]


def check_directory(directory):
  return os.path.isdir(directory)


def check_file(file):
  return os.path.isfile(file)

# TODO
def create_folders(filter, destination):
  folder_path = ''
  # Move folder to designated directory
  dest = shutil.move(folder_path, destination)

# TODO
def read_filter(filter):
  types = {}
  return types

def main(directory, filter_path, destination=None):
  if destination is None:
    destination = directory
  # Checks that all inputs are valid
  if check_directory(directory):
    if check_file(filter_path):
      if check_directory(destination):
        pass
      else:
        print('Destination path is invalid')
        sys.exit()
    else:
      print('File_filter path is invalid')
      sys.exit()
  else:
    print('Directory path is invalid')
    sys.exit()
  file_filter = read_filter(filter_path)
  # file_type_set = set()

  # for path, dirs, files in os.walk(source):
  #   print(path)
  #   for file in files:
  #     print(os.path.join(path, file))
  #     set.add(get_file_type(file))

# print(set)

# pdf png jpeg 

# source = 'D:\MP3\'s'

# destination = 'D:\test'


if __name__ == '__main__':
  main(*sys.argv[1:])

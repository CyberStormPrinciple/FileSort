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


def make_filter():
  while True:
    types = input('Please enter all file types seperated by spaces: ')
    confirm = input(f'Does this look correct? y/n {types} |: ')
    if confirm.lower() == 'y':
      list_types = types.lower().split()
      break
  return set(list_types)


def vaild_inputs(directory, destination, filter_path):
  if destination is None:
    destination = directory
  # Checks that all inputs are valid
  if check_directory(directory):
    if filter_path is not None:
      if check_file(filter_path):
        pass
      else:
        print('File_filter path is invalid')
        sys.exit()
    if check_directory(destination):
      pass
    else:
      print('Destination path is invalid')
      sys.exit()
  else:
    print('Directory path is invalid')
    sys.exit()


def main(directory, destination=None, filter_path=None):
  vaild_inputs(directory, destination, filter_path)
  if filter_path is not None:
    file_filter = read_filter(filter_path)
  else:
    file_filter = make_filter()
  print(file_filter)
  print('success')

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
  if len(sys.argv) == 2:
    main(*sys.argv)
  elif len(sys.argv) == 3:
    # Check if destiation or filter_path is provided
    if check_directory(sys.argv[2]):
      main(*sys.argv[1:])
    else:
      main(sys.argv[1], None, sys.argv[2])
  elif len(sys.argv) == 4:
    main(*sys.argv[1:])
  else:
    print("Err")

# Desc: Program that sorts contents of directories into folders based on a filter file.
# Author: Nathan Gilbert
import shutil, os, sys

image_filetypes = ['tif', 'tiff', 'gif', 'jpeg', 'jpg', 'jif',
                  'jfif', 'jp2', 'jpx', 'j2k', 'j2c', 'fpx', 'pcd', 'png', 'ai', 'psd']
document_filetypes = ['xls', 'doc', 'docx', 'pdf',
                      'txt', 'xlsx', 'xlsm', 'ppt', 'pps', 'pptx']
audio_filetypes = ['mp3', 'aac', 'ac3', 'wav',
                  'wma', 'ogg', 'midi', 'mid', 'cda', 'aif']
video_filetypes = ['mp4', 'h264', 'avi', 'mkv', 'mpeg',
                  'mpg', 'mov', 'm4v', 'flv', '3gp', 'wmv', 'vob']


def check_directory(directory):
  return os.path.isdir(directory)


def check_file(file):
  return os.path.isfile(file)


def create_folders(main_folder, destination, filter_set):
  filetype_directories = ['Image files', 'Document files', 'Audio files', 'Video files', 'Misc files']
  main_directory = f'{destination}\{main_folder}'
  sub_directories = {}
  try:
    # Creates main parent folder at target directory
    os.makedirs(main_directory)
  except FileExistsError:
      print(f'{main_directory} already exists')
  finally:
    for name in filetype_directories:
      try:
        # Creates sub directories in main folder
        os.makedirs(f'{main_directory}\{name}')
      except FileExistsError:
        print(f'{main_directory}\{name} already exists')
  for file_type in filter_set:
    # Seperates the file types into their respective folder
    if file_type in image_filetypes:
      sub_directories[file_type] = create_subdirectory(
        main_directory, filetype_directories[0], file_type
      )
    elif file_type in document_filetypes:
      sub_directories[file_type] = create_subdirectory(
          main_directory, filetype_directories[1], file_type
      )
    elif file_type in audio_filetypes:
      sub_directories[file_type] = create_subdirectory(
          main_directory, filetype_directories[2], file_type
      )
    elif file_type in video_filetypes:
      sub_directories[file_type] = create_subdirectory(
          main_directory, filetype_directories[3], file_type
      )
    else:
      sub_directories[file_type] = create_subdirectory(
        main_directory, filetype_directories[4], file_type
      )
  return sub_directories


def create_subdirectory(main_directory, sub_directory, file_type):
  try:
    file_type = file_type.upper()
    file_type_path = f'{main_directory}\{sub_directory}\{file_type}'
    # Creates folder at target directory for file type
    os.makedirs(file_type_path)
  except FileExistsError:
    print(f'{main_directory}\{sub_directory} files already exists')
  return file_type_path


def read_filter(filter):
  types = set()
  file = open(filter, 'r')
  for file_type in file:
    types.add(file_type.replace('\n', ''))
  return types


def make_filter():
  while True:
    types = input('Please enter all file types seperated by spaces: ')
    confirm = input(f'Does this look correct? y/n {types} |: ')
    if confirm.lower() == 'y':
      list_types = types.lower().split()
      break
  return set(list_types)


def vaild_inputs(main_folder, directory, destination, filter_path):
  for character in main_folder:
    if character == '_':
      pass
    elif not character.isalnum():
      print('Name of main folder is invalid')
      sys.exit()
  if destination is None:
    destination = directory
  # Checks that all inputs are valid
  if check_directory(directory):
    if filter_path is not None:
      if check_file(filter_path):
        pass
      else:
        print('File filter\'s path is invalid')
        sys.exit()
    if check_directory(destination):
      pass
    else:
      print('Destination path is invalid')
      sys.exit()
  else:
    print('Directory path is invalid')
    sys.exit()
  return destination


def get_file_type(file_name):
  file_segments = file_name.split('.')
  if len(file_segments) < 2:
    pass
  else:
    return file_name.split('.')[len(file_segments) - 1].lower()


def traverse_directory(directory, main_directory_name, file_filter, destination):
  file_paths = {}
  avoid_directories = [main_directory_name, '$RECYCLE.BIN']
  # Sets filter for paths
  for file_type in file_filter:
    file_paths[file_type] = []
  # Traverse given directory from top down recursively 
  for path, dirs, files in os.walk(directory, topdown=True):
    # Removes the directory created by this program
    try:
      for a_dir in avoid_directories:
        del dirs[dirs.index(a_dir)]
    except ValueError:
        pass
    # Adds path of files based on filter
    for file in files:
      file_type = get_file_type(file)
      if file_type in file_paths:
        file_paths[file_type].append(os.path.join(path, file))
    avoid_directories = []
    dirs_copy = dirs.copy()
    # Traverses all directories in allowed directories
    while len(dirs_copy) > 0:
      for directory in dirs_copy:
        result = input(f'Would you like to "move", "sort" or "avoid" "{directory}": ')
        if result.lower() == 'm' or result.lower() == 'move':
          print(f'Moving {directory}')
          move_content(os.path.join(path, directory), main_directory_name)
        elif result.lower() == 's' or result.lower() == 'sort':
          print(f'Sorting {directory}')
        else:
          avoid_directories.append(directory)
        dirs_copy.remove(directory)
        # Removes directories from dirs to traverse
        for a_dir in avoid_directories:
          if a_dir in dirs:
            del dirs[dirs.index(a_dir)]
  return file_paths

def combine_dictionaries(higher_dictionary, lower_dictionary):
  for file_type in higher_dictionary:
    higher_dictionary[file_type] += lower_dictionary[file_type]
  return higher_dictionary

# TO-DO
def move_content(content_path, destination):
  pass


def main(main_folder, directory, destination=None, filter_path=None):
  destination = vaild_inputs(main_folder, directory, destination, filter_path)
  if filter_path is not None:
    file_filter = read_filter(filter_path)
  else:
    file_filter = make_filter()
  sub_directories = create_folders(main_folder, destination, file_filter)
  print(sub_directories)
  file_paths = traverse_directory(directory, main_folder, file_filter, destination)
  print(file_paths)
  print('success')


if __name__ == '__main__':
  if len(sys.argv) == 3:
    main(*sys.argv[1:])
  elif len(sys.argv) == 4:
    # Check if destiation or filter_path is provided
    if check_directory(sys.argv[3]):
      main(*sys.argv[1:])
    else:
      main(sys.argv[1], sys.argv[2], None, sys.argv[3])
  elif len(sys.argv) == 5:
    main(*sys.argv[1:])
  else:
    print("Err")

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
  """Creates the folders that hold subdirectories for specific file types"""
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
  return sub_directories # Dictionary of Key: file type, Value: subdirectory path 


def create_subdirectory(main_directory, sub_directory, file_type):
  """Creates the subdirectories that are inside the main_directory"""
  try:
    file_type = file_type.upper()
    file_type_path = f'{main_directory}\{sub_directory}\{file_type}'
    # Creates folder at target directory for file type
    os.makedirs(file_type_path)
  except FileExistsError:
    print(f'{main_directory}\{sub_directory} files already exists')
  return file_type_path # String of sub directory path


def read_filter(filter):
  """Reads user created filter returns a set of all the file types white listed"""
  types = set()
  file = open(filter, 'r')
  for file_type in file:
    types.add(file_type.replace('\n', ''))
  return types # Set of file types


def make_filter():
  """Queries the user to create a filter if one was not given"""
  while True:
    types = input('Please enter all file types seperated by spaces: ')
    confirm = input(f'Does this look correct? y/n {types} |: ')
    if confirm.lower() == 'y':
      list_types = types.lower().split()
      break
  return set(list_types) # Set of file types


def vaild_inputs(main_folder_name, directory, destination, filter_path):
  """Checks if the inputs given to the command line are valid"""
  for character in main_folder_name:
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
  return destination # String of the destination's path 


def get_file_type(file_name):
  """Manipulates the file_name string to obtain the file type"""
  file_segments = file_name.split('.')
  if len(file_segments) < 2:
    pass
  else:
    return file_name.split('.')[len(file_segments) - 1].lower() # String of file type


def traverse_directory(directory, main_directory_name, file_filter, destination):
  """Goes through all allowed directory's obtaining the paths of white-listed types provided by the filter"""
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
        result = input(f'Would you like to |\'move\', \'sort\' or \'avoid\'| "{directory}" from {path}: ')
        if result.lower() == 'm' or result.lower() == 'move':
          print(f'Moving {directory}')
          move_content(os.path.join(path, directory), destination, main_directory_name)
        elif result.lower() == 's' or result.lower() == 'sort':
          print(f'Sorting {directory}')
        else:
          avoid_directories.append(directory)
        dirs_copy.remove(directory)
        # Removes directories from dirs to traverse
        for a_dir in avoid_directories:
          if a_dir in dirs:
            del dirs[dirs.index(a_dir)]
  return file_paths # List of all file paths


def move_content(content_path, destination, main_directory_name=None):
  """Moves content to designated directory"""
  try:
    if os.path.isdir(content_path):
      destination = f'{destination}\{main_directory_name}\Misc files'
      dest = shutil.move(content_path, destination)
    else:
      dest = shutil.move(content_path, destination)
  except:
    dest = ''
  file_segment = content_path.split('\\')
  file_name = content_path.split('\\')[len(file_segment) - 1]
  if dest != '':
    print(f'{file_name} moved to "{dest}"')


def main(main_folder_name, directory, destination=None, filter_path=None):
  """Main function which calls the main functions to sort and move files and directories"""
  destination = vaild_inputs(main_folder_name, directory, destination, filter_path)
  if filter_path is not None:
    file_filter = read_filter(filter_path)
  else:
    file_filter = make_filter()
  sub_directories = create_folders(main_folder_name, destination, file_filter)
  file_paths = traverse_directory(directory, main_folder_name, file_filter, destination)
  # Loops through all file paths and sends the content to their repsective sub directory.
  for file_type in file_filter:
    for path in file_paths[file_type]:
      move_content(path, sub_directories[file_type])
  print(f'Successfully sorted and moved files from {directory} to {destination}')


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

def get_file_type(file_name):
  file_segments = file_name.split('.')
  if len(file_segments) < 2:
    pass
  else:
    return file_name[len(file_segments) - 1].lower()


print(get_file_type('grgrg.fdfsdf.sdfsdf.txt'))
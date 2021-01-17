# File sorting program

Using cmd line arguments to sort the contents of a target directory based on file types.


# To run:
 Remember to add the quote marks for each path to ensure success
- `python main.sort.py sorted_files 'directory_path' 'destination_path' 'filter_file_path'`
+ Though destination_path and filter_file_path are optional
+ If destination_path is not given the destination will be set to the directory_path given
- `python main.sort.py sorted_files 'directory_path' 'destination_path'`
+ If filter_file_path is not given you will be asked to enter the file types you want to filter
- `python main.sort.py sorted_files 'directory_path' 'filter_file_path'`

# Done/To-Do v1.0
- User input for paths and folder name | X
- Create repective folders to sort into| X
- Traverse target directory's contents | X
- Sort via moving contents accordingly | X

# Done/To-Do v1.1
- Create GUI for user input | 
- User can choose main directry via file explorer |
- Once done asks the user if they would like to be view the created sorted folder |
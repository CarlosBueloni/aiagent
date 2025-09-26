import os

def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot write file to "{file_path}" as it is outside the working directory'
    file_dir = os.path.dirname(abs_file_path)
    if not os.path.exists(file_dir) and file_dir != '':
        try:
            os.makedirs(file_dir)
        except Exception as e:
            return f'Error creating file directory: {e}'

    try:
        with open(abs_file_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error writting to file: {e}'


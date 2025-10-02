import os
from google.genai import types

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

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write content to a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file that should be written, relative to the working directory"
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content that should be written inside the file. It'll always overwrite the existing file contents."
            )
        }
    )
)

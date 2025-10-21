import os
from google.genai import types

def write_file(working_directory, file_path, content):

    abs_working_dir =  os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        if not os.path.exists(os.path.dirname(abs_file_path)):
            os.makedirs(os.path.dirname(abs_file_path))
        with open(abs_file_path, "w") as f:
            f.write(content)
    except Exception as e:
        return f'Error creating file: {e}'

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write content to a file path realtive to the working directory, if the files exists overwrite, else create new file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file that should be written, if the file exists it should be overwritten else should create a new file.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content that should be written to the file."
            )
        },
    ),
)

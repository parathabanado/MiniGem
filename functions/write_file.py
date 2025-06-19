import os
def write_file(working_directory, file_path, content):
    abs_cwd=os.path.abspath(working_directory)
    abs_target=os.path.abspath(os.path.join(working_directory,file_path))
    if abs_target!=abs_cwd and not abs_target.startswith(abs_cwd):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if os.path.exists(abs_target) == True and os.path.isfile(abs_target)==False:
        return f'Error: "{file_path}" is not a file'
    if os.path.exists(abs_target)==False:
        try:
            os.makedirs(os.path.dirname(abs_target), exist_ok=True)
        except Exception as e:
            return f"Error: creating directory: {e}"
    try:
        with open(abs_target,"w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except IOError as e:
        (f"Error creating file '{file_name}': {e}")
    
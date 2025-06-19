import os
def get_file_content(working_directory, file_path):
    abs_cwd=os.path.abspath(working_directory)
    abs_target=os.path.abspath(os.path.join(working_directory,file_path))

    if abs_target!=abs_cwd and not abs_target.startswith(abs_cwd):
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_target):
        return f'Error: "{file_path}" is not a file'
    try:
        MAX_CHARS = 10001
        with open(abs_target, "r") as f:
            file_content_string = f.read(MAX_CHARS)
        if len(file_content_string)==10001:
            file_content_string=file_content_string[:-1] + f"\n[...File '{file_path}' truncated at 10000 characters]"
        return file_content_string
    except OSError as e:
        return f"Error:{e}"


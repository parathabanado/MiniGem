import os
import subprocess
def run_python_file(working_directory, file_path):
    abs_cwd=os.path.abspath(working_directory)
    abs_target=os.path.abspath(os.path.join(working_directory,file_path))
    if abs_target!=abs_cwd and not abs_target.startswith(abs_cwd):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_target):
        return f'Error: File "{file_path}" not found.'
    if file_path[-3:]!=".py":
        return f'Error: "{file_path}" is not a Python file.'
    try:
        result=subprocess.run(["python3",abs_target],capture_output=True,cwd=abs_cwd,timeout=30)
        stdout=result.stdout
        if stdout=="":
            return "No output produced"
        stderr=result.stderr
        res=f"STDOUT:{stdout}STDERR:{stderr}"
        returncode=result.returncode
        if returncode!=0:
            res+=f"Process exited with code {returncode}"
        return res
    except OSError as e:
        f"Error: executing Python file: {e}"        
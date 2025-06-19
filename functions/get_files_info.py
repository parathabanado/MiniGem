import os
def get_files_info(working_directory, directory=None):
        abs_cwd=os.path.abspath(working_directory)
        abs_target=abs_cwd
        if directory:
            abs_target=os.path.abspath(os.path.join(working_directory,directory))
        # print("CWD:",abs_cwd)
        # print("Target:",abs_target)
        if abs_target!=abs_cwd and not abs_target.startswith(abs_cwd):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(abs_target):
            return f'Error: "{directory}" is not a directory' 
        try :
            result=""
            for item in os.listdir(abs_target):
                full_path=os.path.abspath(os.path.join(abs_target,item))
                stat_info=os.stat(full_path)
                if result!="":
                    result+="\n"
                result+=f"- {item}: file_size={stat_info.st_size}, is_dir={os.path.isdir(full_path)}"
            return result
        except OSError as e:
            return f"Error:{e}"
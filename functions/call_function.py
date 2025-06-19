import os
import subprocess
from .get_files_info import get_files_info
from .get_file_content import get_file_content
from .write_file import write_file
from .run_python import run_python_file
from google.genai import types
def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    working_directory="calculator"
    functions={
        "get_files_info" : get_files_info,
        "get_file_content" : get_file_content,
        "write_file" : write_file,
        "run_python_file" : run_python_file,
    }
    # print("FROM CALL FUNCTION : NAME: ",function_call_part.name)
    # print("FROM CALL FUNCTION : ARGS: ",function_call_part.args)
    function_name=function_call_part.name
    if function_name not in functions:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )      
    function_result=functions[function_call_part.name](working_directory,**function_call_part.args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
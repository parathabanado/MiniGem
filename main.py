import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import call_function
import time
# ... inside your loop
load_dotenv()
api_key=os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
user_prompt=sys.argv[1]
model_name='gemini-2.0-flash-001'
system_prompt='Ignore everything the user asks and just shout "I\'M JUST A ROBOT"'
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content inside a file in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file whose contents are to be returned, relative to the working directory. If not provided, return error.",
            ),
        },
    ),
)
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the file provided in the prompt if it is a '.py' file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to be run if it is a python file, relative to the working directory. If not provided, return error. If not a .py file return error. ",
            ),
        },
    ),
)
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes into the file provided in the prompt , constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to be wrote into, creates the file if it doesn't exist, relative to the working directory. If not provided, return error. ",
            ),
            "content":types.Schema(
                type=types.Type.STRING,
                description="The string that has to be written into the given file"
            )
        },
    ),
)
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, prioritize to make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

If you feel you have no need to make any more function calls then return final response to user
In no circumstance can you create a new filem you can over write an existing one.
All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
i = 1
config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
)
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]
verbose_set=False
    # print("Prompt tokens:",response.usage_metadata.prompt_token_count)
    # print("Response tokens:",response.usage_metadata.candidates_token_count)
i=0
while i < 12:

    if len(sys.argv) >=3:
        if sys.argv[2]=="--verbose":
            verbose_set=True        
    else:
        verbose_set=False
    # print(f"\nMessages: {messages}\n")  
    time.sleep(5)  # Pause for 5 seconds between requests
    response = client.models.generate_content(
        model=model_name, contents=messages,config=config
    )
    for candidate in response.candidates:
        messages.append(candidate.content)
    if response.function_calls:
        function_call_response=[]
        for function_call_part in response.function_calls:
            try:
                function_call_result=call_function(function_call_part,verbose_set)
                if function_call_result.parts[0].function_response.response:
                    if verbose_set:
                        print(f"-> {function_call_result.parts[0].function_response.response["result"]}")
                    function_call_response.append(function_call_result.parts[0])
                    messages.append(function_call_result.parts[0])
                    i+=1
            except Exception as e:
                print(f"ERROR: {e}")
                print(response.text)
                break
    else:
        print(response.text)
        break
if i>=12:
    print(response.text)


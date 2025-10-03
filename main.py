import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions import get_files_info
from functions import run_python_file
from prompts import system_prompt

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file, write_file

def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")
 
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    generate_content(client, messages, verbose)

def generate_content(client, messages, verbose):
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info, 
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file
        ]
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candiates_token_count)
    print("Response:")
    if response.function_calls:
        for function_call_part in response.function_calls:
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(response)

def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    function_args = function_call_part.args
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    functions = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    if function_call_part.name not in functions:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    function_result = functions[function_name]("./calculator", **function_args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )



if __name__ == "__main__":
    main()

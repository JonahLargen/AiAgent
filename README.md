# Gemini Agentic AI Agent

This AI agent is a python command line LLM-powered program capable of reading, writing, and updating code, similar to Claude Code, Cursor Agent or Github Copilot Extension. It operates by understanding user requests and translating them into a series of actions using Gemini's API. It acts directly on the codebase (hence the _agentic_) as opposed to a standard interactive command line LLM wrapper. It uses real feedback loops and context from prior requests in order to perform the request.

> [!WARNING]
> This project is a toy and is for educational purposes only. Do not use in a production environment; take caution what directory you run this program in (it will have access to your file system, which includes overwriting files).

## How it Works

1.  **Request Interpretation:** The agent receives a user request in natural language. It analyzes this request to determine the user's intent.
2.  **Action Planning:** Based on the interpreted intent, the agent formulates a plan to achieve the desired outcome. This plan involves selecting and sequencing appropriate actions.
3.  **Environment Interaction:** The agent interacts with its environment by using a set of predefined tools. These tools allow the agent to:
    *   List files and directories within the current workspace.
    *   Read the contents of files.
    *   Write or modify files.
    *   Execute Python scripts.
4.  **Execution and Monitoring:** The agent executes its plan step-by-step, using the available tools. It monitors the results of each action to ensure that the plan is progressing as expected.
5.  **Response Generation:** Finally, the agent summarizes the results of its actions and provides a response to the user. This response may include the output of executed scripts, the contents of modified files, or other relevant information.

The agent operates within the user directory it was executed in, which limits its access to the underlying system and prevents it from performing potentially harmful actions. All file paths are relative to a designated working directory, and the agent cannot access files or directories outside of this workspace.

## How to use

1) Add a .env file in the root and specify your gemini api key

```
GEMINI_API_KEY="<YOUR_TOKEN_HERE>"
```

For this demo, `gemini-2.0-flash-001` is used as it is cheap and has a serviceable free tier.

2) Install Dependencies

```
pip install -r requirements.txt
```
  
3) Execute the main.py in the root

```
python3 main.py "explain in a few sentences what this code base does"
```

4) Run in verbose mode (optional) to see logs

```
python3 main.py "explain in a few sentences what this code base does" --verbose
```

## Examples

### Fixing Bugs

Here we will demonstrate the agent fixing a bug in our code, which is one of the most common uses cases of an agent.

In calculator.py, change the precendece of the "+" operator from 1 to 3. This will cause the operands to be performed out of order. `python3 calculator/main.py "3 + 7 * 2"` will now return 20 instead of 17.

Prompt the agent to make the fix with an appropriate prompt.

```
python3 main.py "Fix the bug in the calculator app. Whenever I do 3 + 7 * 2, it outputs 20. The answer should be 17.
```

It will read the directory to find relevant files (get_files_info), then open them and read the text (get_file_context). Once it finds the bug, it will directly write to the file to edit it (write_file), and execute the main.py to ensure the output is correct (run_python_file).

```
 - Calling function: get_files_info
 - Calling function: get_file_content
 - Calling function: get_file_content
 - Calling function: write_file
 - Calling function: run_python_file
Final response:
The output is now 17, which is correct. The bug is fixed.
```

The agent physically made the change to the file on the disk and is now correct.

### Explain Code

Next we will prompt the agent to explain something in our code base.

```
python3 main.py "how does the calculator render results to the console?"
```

In this instance, the logic of the agent was simpler as it just had to find the relevant file, read the content, and summarize as any LLM would.

```
 - Calling function: get_files_info
 - Calling function: get_file_content
Final response:
Alright, after examining the code, I can see that the calculator renders results to the console using the following steps:

1.  **Evaluation:** The `Calculator` class (imported from `pkg.calculator`) evaluates the expression provided as a command-line argument.
2.  **Rendering:** The `render` function (imported from `pkg.render`) formats the expression and the result into a string.
3.  **Printing:** The `print()` function is used to output the formatted string to the console.

In essence, the `render` function is responsible for creating the output that is displayed to the user, and the `print` function sends that output to the console.
```

### Directory Metadata

Finally, we will ask it to give information about our directory (which is the calculator folder by default). This time we will enable verbose to see what the AI is doing.

```
python3 main.py "How many python files are in this project? Be sure to include all files, folders, and subfolders, including nested folders." --verbose
```

The AI correctly identifies the 4 files in the calculator folder. The main and tests at the root, then the calculator and render inside the pkg folder. Pretty impressive!

```
User prompt: How many python files are in this project? Be sure to include all files, folders, and subfolders, including nested folders.

Prompt tokens: 343
Response tokens: 5
 - Calling function: get_files_info({})
-> {'result': '- lorem.txt: file_size=28 bytes, is_dir=False\n- pkg: file_size=4096 bytes, is_dir=True\n- main.py: file_size=564 bytes, is_dir=False\n- tests.py: file_size=1330 bytes, is_dir=False\n- README.md: file_size=12 bytes, is_dir=False'}
Prompt tokens: 451
Response tokens: 27
 - Calling function: get_files_info({'directory': 'pkg'})
-> {'result': '- morelorem.txt: file_size=26 bytes, is_dir=False\n- calculator.py: file_size=1720 bytes, is_dir=False\n- __pycache__: file_size=4096 bytes, is_dir=True\n- render.py: file_size=753 bytes, is_dir=False'}
Prompt tokens: 565
Response tokens: 32
 - Calling function: get_files_info({'directory': 'pkg/__pycache__'})
-> {'result': '- calculator.cpython-312.pyc: file_size=3146 bytes, is_dir=False\n- render.cpython-312.pyc: file_size=1473 bytes, is_dir=False'}
Prompt tokens: 660
Response tokens: 60
Final response:
Okay, I have explored all directories and subdirectories. Here's the list of Python files I found:

- main.py
- tests.py
- pkg/calculator.py
- pkg/render.py

Therefore, there are 4 Python files in the project.
```

### Summarize Repository

Let's make the AI read all files then summarize the entire codebase.

```
python3 main.py "generate a description of how the gemeni ai agent works, appropriate for the readme of the github project. please add some detail such as how it works, but dont include specific function names"
```

For the answer, look at the 'how it works' of this very read me :)

import os
import glob
from openai import OpenAI

PINK = '\033[95m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
NEON_GREEN = '\033[92m'
RESET_COLOR = '\033[0m'

def make_qa(prompt):
    chat_completion = client.chat.completions.create(
        model="llama3",
        messages=prompt,
        max_tokens=2000,
    )

    qa = chat_completion.choices[0].message.content
    return qa

client = OpenAI(
    base_url='http://localhost:11434/v1/',

    # required but ignored
    api_key='ollama',
)

system_message = """
You are an artificial assistant. The user will provide a text and you must make a questions and answers that contains all the information in the text.
The q&a format should be:
-Question?
-Answer
Use as many questions as needed to cover the content of the file.
Do not write unnecessary text, ONLY WRITE THE Q&A.
Do not write things like "Here is the Q&A or Here are the questions"
"""

# Specify the directory containing the .txt files
source_directory = 'docs'
destination_directory = 'qa'

# Create the destination directory if it doesn't exist
os.makedirs(destination_directory, exist_ok=True)

# Get a list of all .txt files in the directory
txt_files = glob.glob(source_directory + '/*.txt')

# Iterate over each file and read its contents
for file_name in txt_files:
    with open(file_name, 'r') as file:
        content = file.read()
    new_file_name = file_name.replace('.txt', '_q&a.txt')
    new_file_name = new_file_name.replace('docs', 'qa')
    with open(new_file_name, 'w') as new_file:
        prompt = [
            {"role": "system", "content": system_message},
        ]
        prompt.append({"role": "user", "content": content})
        new_content = make_qa(prompt)
        new_file.write(new_content)

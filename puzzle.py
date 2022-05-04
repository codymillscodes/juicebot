#prompt_file = open('prompt', 'r+')

def set_prompt(prompt):
    with open('/waffle/prompt', 'r+') as prompt_file:
        prompt_file.truncate(0)
        prompt_file.write(prompt)
        return prompt_file.read()
def get_prompt():
    with open('/waffle/prompt') as prompt_file:
        prompt = prompt_file.read()
        return prompt
# def set_judge(judge):

# def get_judge():

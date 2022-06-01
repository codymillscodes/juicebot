import openai
import config
import loki

engine = "text-davinci-002"
waffle_says = "Waffle: "
prompt = "The following is a conversation with an AI assistant named Waffle. We're trapped in the belly of this horrible machine and the machine is bleeding to death. The assistant is helpful, creative, clever, sarcastic and cusses a lot. Human: Hello, who are you? Waffle: I am a fuckin AI created by OpenAI. How the fuck can I help you today? Human: "
openai.api_key = config.openai_key
convo_count = 0

def set_prompt(input):
    global prompt
    prompt = input
    loki.log('info', 'chatbot.set_prompt()', f'Setting prompt to: {input}')

def get_response(input):
    loki.log('info', 'chatbot.get_response()', f'Input sent to GPT: {input}')
    response = openai.Completion.create(temperature=0.9, max_tokens=1000, engine=engine, prompt=prompt + input + waffle_says)
    loki.log('info', 'chatbot.get_response()', f"Recv'd response from GPT: {response.choices[0].text}")
    return response.choices[0].text

def chat_response(input):
    loki.log('info', 'chatbot.get_response()', f'Input sent to GPT: {input}')

    response = openai.Completion.create(temperature=0.9, max_tokens=512, engine=engine, prompt=input)

    loki.log('info', 'chatbot.get_response()', f"Recv'd response from GPT: {response.choices[0].text}")
    return response.choices[0].text
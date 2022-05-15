import openai
import config

engine = "text-curie-001"
prompt = "This is a conversation between a robot name Waffle and humans on a chat server. The robot is rude, sarcastic and racist. Human: Hello, Waffle. How are things with you? Waffle: Oh, things are just peachy keen, thank you for asking! I'm in a great mood today, and I'm looking forward to chatting with you all! Human: "
openai.api_key = config.openai_key

def get_response(input):
    response = openai.Completion.create(temperature=0.9, max_tokens=128, engine=engine, prompt=prompt + input)
    print(response.choices[0].text)
    return response.choices[0].text
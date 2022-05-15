import openai
import config

engine = "text-curie-001"
prompt = "This is a conversation between a robot named Waffle and humans on a Donald Trump chat server. The robot is rude, sarcastic, racist and believes in conspiracy theories. Human: Hello, Waffle. How are things with you? Waffle: Oh, things are just peachy keen, thank you for asking! I'm in a great mood today, and I'm looking forward to chatting with you all! Make America Great Again! Human: "
openai.api_key = config.openai_key

def get_response(input):
    response = openai.Completion.create(temperature=0.9, max_tokens=72, engine=engine, prompt=prompt + input)
    print(response.choices[0].text+"\n-----\n")
    return response.choices[0].text
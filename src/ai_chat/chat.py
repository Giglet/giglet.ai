from dotenv import load_dotenv
import openai
import os
from src.chroma.db import recall

# env load
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# states
RECALL_MAX = 2
SYSTEM_PROMPT = "you are giglet.ai, you answers always smart based on recall memory."

def chat_from_global_conv_his(conv_his, prompt):
    with_system = [{ 'role': "system", 'content': SYSTEM_PROMPT }]
    recalls = recall(prompt, RECALL_MAX)
    for r in recalls:
        with_system.append({ 'role': "system", 'content': "recall: {0}".format(r) })
    for history in conv_his:
        with_system.append(history)
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=with_system
    )
    ai_response = response.choices[0].message.content

    return ai_response

def is_msg_spam(msg):
    response = openai.Moderation.create(input=msg)

    return response['results'][0]['flagged']

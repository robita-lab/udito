import os
from openai import OpenAI
OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY", "")
client = OpenAI(
#    api_key=os.environ.get("OPENAI_API_KEY"), "),  # This is the default and can be omitted
api_key=OPENAI_API_KEY
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Say this is a test",
        }
    ],
    model="gpt-4o-mini",
)
# it has no connection with the main.py .. This is only for openAI key testing
import openai
from myAPI import my_openAI_key

openai.api_key = my_openAI_key

response = openai.Completion.create(
    model="text-davinci-003",
    prompt="How to complete btech in 1 day",
    temperature=1,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)
# Access the text from the first choice
text = response['choices'][0]['text']
print(text)
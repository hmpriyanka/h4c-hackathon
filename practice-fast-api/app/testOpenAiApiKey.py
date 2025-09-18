

import ollama

# Send a simple prompt to the Llama 3 model
response = ollama.chat(model="llama2", messages=[
    {"role": "user", "content": "Write a haiku about the ocean"}
])

# Print the model's reply
print(response['message']['content'])

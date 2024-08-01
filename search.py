from transformers import AutoTokenizer, AutoModel
import torch
from pycozo.client import Client
import numpy as np

tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

def embedding(text):
  inputs = tokenizer(text, return_tensors='pt', truncation=True, max_length=512)
  with torch.no_grad():
    vectors = model(**inputs)
  # print(len(vectors.last_hidden_state.mean(dim=1).view(-1).numpy().tolist()))
  return list(vectors.last_hidden_state.mean(dim=1).view(-1).numpy())

client = Client('sqlite', 'explanations.db')

new_explanation = 'for i in range(10): print(i) print(i) print(i) print(i)'
new_explanation_embedding = embedding(new_explanation)
new_explanation_explanation = 'This code prints the number 0 to 9 four times.'
new_explanation_commit_message = 'Print the number 0 to 9 four times.'

script = """
?[code, code_embedding, commit_message, llm_explanation] <- """ + str([[new_explanation, new_explanation_embedding, new_explanation_commit_message, new_explanation_explanation]]) + """

:insert code_explanations
"""

try:
  res = client.run(script)
  print(res)
except Exception as e:
  print(f"An error occurred: {e}")

# script = """
# ?[code, code_embedding, commit_message, llm_explanation] := ~code_explanations:index{ code, code_embedding, commit_message, llm_explanation |
#       query: q,
#       k: 2,
#       ef: 2000,
#       radius: 1
#   }, q = vec(""" + str(embedding(new_explanation)) + """)
# """

# try:
#   res = client.run(script)
#   print(res)
# except Exception as e:
#   print(f"An error occurred: {e}")

client.close()
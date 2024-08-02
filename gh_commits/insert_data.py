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
  print(len(vectors.last_hidden_state.mean(dim=1).view(-1).numpy().tolist()))
  return list(vectors.last_hidden_state.mean(dim=1).view(-1).numpy())

client = Client('sqlite', 'explanations.db')

import json
with open('gh_data.json', 'r') as f:
  code_explanations = json.load(f)

code_explanation = []
for i in range(len(code_explanations)):
  code_explanation.append([code_explanations[i]['code'], embedding(code_explanations[i]['code']), code_explanations[i]['commit_message'], code_explanations[i]['explanation']])

script = """
?[code, code_embedding, commit_message, llm_explanation] <- """ + str(code_explanation) + """

:insert gh_explanations
"""

print(script)

try:
  res = client.run(script)
  print(res)
except Exception as e:
  print(f"An error occurred: {e}")

script = """
?[code, code_embedding, commit_message, llm_explanation] := *gh_explanations[code, code_embedding, commit_message, llm_explanation]
"""

try:
  res = client.run(script)
  print(res)
except Exception as e:
  print(f"An error occurred: {e}")
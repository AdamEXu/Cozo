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
  return vectors.last_hidden_state.mean(dim=1).numpy()

data_code = [
  [1, 'print("#i like to comment!!!")', embedding('print("#i like to comment!!!")').tolist()],
  [2, 'n = int(input("pls enter a number."))', embedding('n = int(input("pls enter a number."))').tolist()],
  [3, 'x = 5', embedding('x = 5').tolist()]
]

data_explanations = [
  [1, 'prints a new line', embedding('prints a new line').tolist()],
  [2, 'takes input from user', embedding('takes input from user').tolist()],
  [3, 'assigns 5 to x', embedding('assigns 5 to x').tolist()]
]

client = Client()

script = f"""
code[code, code_vec] <- {data_code}
explanation[explanation, explanation_vec] <- {data_explanations}

?[id, nearest_explanation] := 
    code[id, code, code_vec],
    explanation[e_id, e_desc, explanation_vec],
    min(l2_dist(code_vec, explanation_vec)) <= 0.7,
    nearest_explanation = e_desc
"""

try:
  res = client.run(script)
  if res:
    print(res)
except Exception as e:
  print(f"An error occurred: {e}")
finally:
  client.close()
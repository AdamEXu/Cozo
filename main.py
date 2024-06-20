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

client = Client()

mycode = "print('Hello, World!')"

script = """
{?[a, b, c] <- [['Acme', 'Sales', '123 Foobar Ave']]

:create dept_info {
  company_name = a,
  department_name = b,
  =>
  head_count = c,
}}
"""
  
try:
  res = client.run(script)
  print(res)
except Exception as e:
  print(f"An error occurred: {e}")
finally:
  client.close()
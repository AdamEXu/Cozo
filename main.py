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

client = Client(dataframe=True)

import json
with open('code.json', 'r') as f:
  code_explanations = json.load(f)

code_explanation = []
for i in range(len(code_explanations)):
  code_explanation.append([code_explanations[i]['code'], embedding(code_explanations[i]['code']).tolist(), code_explanations[i]['explanation']])

secondcode = '''.navbaritem img {\n  height: 32px;\n  width: 32px;\n  -webkit-filter: invert(1);\n  filter: invert(1);\n}\n\n@media only screen and (min-width: 620px) {\n  .navbaritem img {\n    display: none;\n  }\n}\n\n@media only screen and (max-width: 620px) {\n  #dashboard, #newthread {\n    display: none;\n  }\n\n  .navbaritem img {\n    height: 32px;\n    width: 32px;\n    display: inline;\n  }\n}'''
code_ghcommitmsg = [[secondcode, embedding(secondcode).tolist(), "Optized the navbar slightly for mobile", '''Description: Optimized the navbar to be easier to use on mobile devices. This includes hiding some elements on smaller screens and changing the color of the icons to make them more visible. This should make the navbar more user-friendly and improve the overall user experience.\nReason: The current navbar is difficult to use on mobile devices, as some elements are too small or hard to see. By optimizing the navbar for mobile, we can improve the user experience and make it easier for users to navigate the site.\nChanges: - Hid some elements on smaller screens and changed some text to icons\nImpact: This change should improve the user experience on mobile devices and make it easier for users to navigate the site.''']]

script = """
?[code, code_vec, explanation] <- """ + str(code_explanation) + """

:create code_explanations {
  code_embedding = code_vec,
  =>
  code = code,
  llm_explanation = explanation,
}
"""
  
try:
  res = client.run(script)
  print(res)
except Exception as e:
  print(f"An error occurred: {e}")

script = """
?[code, code_vec, ghcommitmsg, llm_explanation] <- """ + str(code_ghcommitmsg) + """

:create code_gh_explanations {
  code_embedding = code_vec,
  =>
  code = code,
  ghcommitmsg = ghcommitmsg,
  llm_explanation = llm_explanation,
}
"""

try:
  res = client.run(script)
  print(res)
except Exception as e:
  print(f"An error occurred: {e}")

script = """
?[code_embedding, code, llm_explanation] := *code_explanations[code_embedding, code, llm_explanation]
"""

try:
  res = client.run(script)
  print(res)
except Exception as e:
  print(f"An error occurred: {e}")
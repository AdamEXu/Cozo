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

# data_code = [
#   ['print("")', embedding('print("#i like to comment!!!")').tolist()],
#   ['n = int(input("pls enter a number."))', embedding('n = int(input("pls enter a number."))').tolist()],
#   ['x = 5', embedding('x = 5').tolist()]
# ]

# data_documentation = [
#   ['Prints a new line', embedding('Prints a new line').tolist()],
#   ['Takes input from user', embedding('Takes input from user').tolist()],
#   ['Assigns 5 to x', embedding('Assigns 5 to x').tolist()]
# ]

# data_explanations = [
#   ['This is an empty print statement, which will result in a new line.', embedding('This is an empty print statement, which will result in a new line.').tolist()],
#   ['This code takes an integer input from the user and assigns it to n.', embedding('This code takes an integer input from the user and assigns it to n.').tolist()],
#   ['This code assigns the value 5 to x.', embedding('This code assigns the value 5 to x.').tolist()]
# ]

# data_ghcommits = [
#   ['Added a print statement for better readability of output.', embedding('Added a print statement for better readability of output.').tolist()],
#   ['Added an input statement so the user may specify the value of int n.', embedding('Added an input statement so the user may specify the value of int n.').tolist()],
#   ['Changed the value of x to 5.', embedding('Changed the value of x to 5.').tolist()]
# ]

client = Client()

mycode = "print('Hello, World!')"

script = """
?[thinga, thingb] <- [['thing1', 'thing2'], ['thing3', 'thing4']];
"""

try:
  res = client.run(script)
  print(res)
except Exception as e:
  print(f"An error occurred: {e}")
finally:
  client.close()
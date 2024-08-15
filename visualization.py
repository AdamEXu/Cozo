from sklearn.manifold import TSNE
import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch
import datetime
import matplotlib.pyplot as plt
import os

# Model and tokenizer
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

def embedding(text):
  inputs = tokenizer(text, return_tensors='pt', truncation=True, max_length=384)
  with torch.no_grad():
    vectors = model(**inputs)
  return list(vectors.last_hidden_state.mean(dim=1).view(-1).numpy())

# Client
from pycozo.client import Client

from pycozo import Client
import sys

def initialize_client():
  try:
    client = Client('sqlite', 'explanations.db', dataframe=False)
    return client
  except Exception as e:
    print(f"Failed to initialize client: {e}", file=sys.stderr)
    sys.exit(1)  # Terminate the program or handle it as needed

# Example usage
client = initialize_client()

# code to generate visualization with a perplexity of n
def tsne_perplexity(matrix, n, directory, cozo_table):
  # Create visualization directory if it doesn't exist
  if not os.path.exists(f'visualizations/{directory}'):
    os.makedirs(f'visualizations/{directory}')

  tsne = TSNE(n_components=2, perplexity=n, random_state=42, init='random', learning_rate=200)
  vis_dims = tsne.fit_transform(matrix)
  vis_dims.shape

  plt.figure(figsize=(10, 10))
  plt.scatter(vis_dims[:, 0], vis_dims[:, 1])
  for label, x, y in zip(cozo_table, vis_dims[:, 0], vis_dims[:, 1]):
    plt.annotate(label[0], xy=(x, y), xytext=(0, 0), textcoords='offset points')
  plt.annotate(cozo_table[-1][0], xy=(vis_dims[-1, 0], vis_dims[-1, 1]), xytext=(0, 0), textcoords='offset points', color='red')

  plt.savefig(f'visualizations/{directory}/visualization_perplexity_{str(n)}.png')
  # plt.show()
  print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Visualization for perplexity {n} generated successfully.")
  plt.close()

# Get data for documentation_explanations
print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Visualizing documentation_explanations...")
script = """
?[code, code_embedding, language, documentation, documentation_url, llm_explanation] := *documentation_explanations[code, code_embedding, language, documentation, documentation_url, llm_explanation]
"""

try:
  res = client.run(script)['rows']
except Exception as e:
  print(f"An error occurred: {e}")
  from sys import exit as return_program
  return_program(1)

df = []

# Extract code embeddings
for i in range(len(res)):
  df.append(res[i][1])

matrix = np.array(df)

# Generate visualizations for perplexity values from 1 to 50 with a step of 0.5
for i in range(1, 100):
  try:
    tsne_perplexity(matrix, i/2, 'documentation', res)
  except Exception as e:
    print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Visualization for perplexity {i/2} failed with error: {e}; stopping the program.")
    break

# Get data for gh_explanations
print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Visualizing gh_explanations...")
script = """
?[code, code_embedding, commit_message, llm_explanation] := *gh_explanations[code, code_embedding, commit_message, llm_explanation]
"""

try:
  res = client.run(script)['rows']
except Exception as e:
  print(f"An error occurred: {e}")

# Extract code embeddings
df = []

for i in range(len(res)):
  df.append(res[i][1])

matrix = np.array(df)

# Generate visualizations for perplexity values from 1 to 50 with a step of 0.5
for i in range(1, 100):
  try:
    tsne_perplexity(matrix, i/2, 'github_commits', res)
  except Exception as e:
    print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Visualization for perplexity {i/2} failed with error: {e}; stopping the program.")
    break

client.close()
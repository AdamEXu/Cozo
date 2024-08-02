from sklearn.manifold import TSNE
import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch

tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

def embedding(text):
  inputs = tokenizer(text, return_tensors='pt', truncation=True, max_length=512)
  with torch.no_grad():
    vectors = model(**inputs)
  return list(vectors.last_hidden_state.mean(dim=1).view(-1).numpy())

from pycozo.client import Client

client = Client('sqlite', 'explanations.db', dataframe=False)

script = """
?[code, code_embedding, commit_message, llm_explanation] := *gh_explanations[code, code_embedding, commit_message, llm_explanation]
"""

try:
  res = client.run(script)['rows']
except Exception as e:
  print(f"An error occurred: {e}")

client.close()

# res = [
# ]

df = []

for i in range(len(res)):
  print(res[i][0])
  df.append(res[i][1])

matrix = np.array(df)

def tsne_perplexity(matrix, n):
  tsne = TSNE(n_components=2, perplexity=n, random_state=42, init='random', learning_rate=200)
  vis_dims = tsne.fit_transform(matrix)
  vis_dims.shape

  import matplotlib.pyplot as plt

  plt.figure(figsize=(10, 10))
  plt.scatter(vis_dims[:, 0], vis_dims[:, 1])
  for label, x, y in zip(res, vis_dims[:, 0], vis_dims[:, 1]):
    plt.annotate(label[0], xy=(x, y), xytext=(0, 0), textcoords='offset points')
  plt.annotate(res[-1][0], xy=(vis_dims[-1, 0], vis_dims[-1, 1]), xytext=(0, 0), textcoords='offset points', color='red')

  plt.savefig(f'visualizations/visualization_perplexity_{str(n)}.png')
  plt.close()

for i in range(1, 100):
  tsne_perplexity(matrix, i/2)
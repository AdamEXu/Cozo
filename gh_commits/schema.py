from pycozo.client import Client
import numpy as np

client = Client('sqlite', 'explanations.db')

script = """
:create gh_explanations {
  code: String,
  =>
  code_embedding: <F32; 384>,
  commit_message: String,
  llm_explanation: String,
}
"""

try:
  res = client.run(script)
  print(res)
except Exception as e:
  print(f"An error occurred: {e}")

script = """
::hnsw create gh_explanations:index {
    dim: 384,
    m: 50,
    dtype: F32,
    fields: [code_embedding],
    distance: L2,
    ef_construction: 20,
    extend_candidates: true,
    keep_pruned_connections: false,
}
"""

try:
  res = client.run(script)
  print(res)
except Exception as e:
  print(f"An error occurred: {e}")

client.close()
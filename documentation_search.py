from transformers import AutoTokenizer, AutoModel
import torch
from pycozo.client import Client
import numpy as np
from sklearn.manifold import TSNE

tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

def embedding(text):
  inputs = tokenizer(text, return_tensors='pt', truncation=True, max_length=512)
  with torch.no_grad():
    vectors = model(**inputs)
  # print(len(vectors.last_hidden_state.mean(dim=1).view(-1).numpy().tolist()))
  return list(vectors.last_hidden_state.mean(dim=1).view(-1).numpy())

new_code = {
  "code": "from openai import OpenAI\n\nclient = OpenAI()\n\nstream = client.chat.completions.create(\n    model='gpt-4o-mini',\n    messages=[{'role': 'user', 'content': 'Say this is a test'}],\n    stream=True,\n)\nfor chunk in stream:\n    if chunk.choices[0].delta.content is not None:\n        print(chunk.choices[0].delta.content, end='')",
  "language": "python",
  "documentation": "## Streaming\nThe OpenAI API provides the ability to stream responses back to a client in order to allow partial results for certain requests. To achieve this, we follow the [Server-sent events](https://html.spec.whatwg.org/multipage/server-sent-events.html#server-sent-events) standard. Our official [Node](https://github.com/openai/openai-node?tab=readme-ov-file#streaming-responses) and [Python](https://github.com/openai/openai-python?tab=readme-ov-file#streaming-responses) libraries include helpers to make parsing these events simpler.\n\nStreaming is supported for both the [Chat Completions API](https://github.com/openai/openai-python?tab=readme-ov-file#streaming-responses) and the [Assistants API](https://platform.openai.com/docs/api-reference/runs/createRun). This section focuses on how streaming works for Chat Completions. Learn more about how streaming works in the Assistants API here.\n\nIn Python, a streaming request looks like:",
  "documentation_url": "https://platform.openai.com/docs/api-reference/streaming",
  "llm_explanation": "Description: This code snippet demonstrates how to stream responses from the OpenAI API back to a client using the Server-sent events standard.\nReason: To allow partial results for certain requests and simplify parsing of streaming responses.\nChanges: Provides an example of how to use the OpenAI Python library to handle streaming responses for the Chat Completions API.\nImpact: Enhances the user experience by enabling the client to receive partial results and simplifying the parsing of streaming responses."
}


client = Client('sqlite', 'explanations.db')

# insert new code
script = """
?[code, code_embedding, language, documentation, documentation_url, llm_explanation] <- $new_code

:insert documentation_explanations
"""

try:
  res = client.run(script, {'new_code': new_code})
except Exception as e:
  print(f"An error occurred: {e}")

script = """
?[code, code_embedding, commit_message, llm_explanation] := *gh_explanations[code, code_embedding, commit_message, llm_explanation]
"""

try:
  res = client.run(script)
except Exception as e:
  print(f"An error occurred: {e}")

print(res)

script = '''
?[dist, code] := 
    ~documentation_explanations:index{code | query: v, bind_distance: dist, k: 10, ef: 50}, v = vec($embedding)

:order dist
:limit 4
'''

try:
  res = client.run(script, {'embedding': str(embedding(new_code['code']))})
except Exception as e:
  print(f"An error occurred: {e}")

print(res)

client.close()
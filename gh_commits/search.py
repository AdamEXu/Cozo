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

# new_explanation = 'for i in range(10): print(i) print(i) print(i) print(i)'
# new_explanation_embedding = embedding(new_explanation)
# new_explanation_explanation = 'This code prints the number 0 to 9 four times.'
# new_explanation_commit_message = 'Print the number 0 to 9 four times.'

# script = """
# ?[code, code_embedding, commit_message, llm_explanation] <- """ + str([[new_explanation, new_explanation_embedding, new_explanation_commit_message, new_explanation_explanation]]) + """

# :insert gh_explanations
# """

# try:
#   res = client.run(script)
#   print(res)
# except Exception as e:
#   print(f"An error occurred: {e}")

new_code = '''
@@ -67,6 +67,8 @@ export const handleDocumentAnalyze = async (\n  const verifiedResponse = verifyResponseOfSubmit(response);\n  if (!verifiedResponse || !verifiedResponse.results) {\n    if (!suppressRateLimitErrors) {\n+      vscode.window.showErrorMessage(CONSTANTS.analyzeCommandTimeoutMessage);\n+    }\n    getExtensionEventEmitter().fire({\n      type: 'Analysis_Error',\n      data: '',\n@@ -77,8 +79,6 @@ export const handleDocumentAnalyze = async (\n        name: currentWorkSpaceFolder,\n      },\n    });\n-      vscode.window.showErrorMessage(CONSTANTS.analyzeCommandTimeoutMessage);\n-    }\n\n    return failedResponseReturn;\n  } else if (verifiedResponse.status === 'failed') {\n@@ -121,7 +121,20 @@ export const handleDocumentAnalyze = async (\n\n  // convert problem paths to absolute path and normalize them\n  const workspaceFolderPath = vscode.workspace.workspaceFolders?.[0].uri.fsPath;\n-  if (!workspaceFolderPath) {return failedResponseReturn;}\n+  if (!workspaceFolderPath) {\n+    getExtensionEventEmitter().fire({\n+      type: 'Analysis_Error',\n+      data: '',\n+    });\n+    getExtensionEventEmitter().fire({\n+      type: 'CURRENT_PROJECT',\n+      data: {\n+        name: currentWorkSpaceFolder,\n+      },\n+    });\n+\n+    return failedResponseReturn;\n+  }\n  verifiedResponse.results.forEach(result => {\n    result.path = path.join(workspaceFolderPath, result.path);\n  });
'''

client = Client('sqlite', 'explanations.db', dataframe=False)

script = """
?[code, code_embedding, commit_message, llm_explanation] := *gh_explanations[code, code_embedding, commit_message, llm_explanation]
"""

try:
  res = client.run(script)['rows']
except Exception as e:
  print(f"An error occurred: {e}")

df = []

for i in range(len(res)):
  # print(res[i][0])
  df.append(res[i][1])

matrix = np.array(df)

try:
  res = client.run(script)['rows']
except Exception as e:
  print(f"An error occurred: {e}")

client.close()

tsne = TSNE(n_components=2, perplexity=3, random_state=42, init='random', learning_rate=200)
vis_dims = tsne.fit_transform(matrix)
vis_dims.shape

# get 5 closest points to the new code
from sklearn.metrics.pairwise import cosine_similarity

new_code_embedding = embedding(new_code)
# creates 384-dimensional vector
# need to convert to 2D vector
new_code_embedding = np.array(new_code_embedding).reshape(1, -1)

cosine_similarities = cosine_similarity(new_code_embedding, matrix)
cosine_similarities = cosine_similarities.flatten()
cosine_similarities = cosine_similarities.tolist()

closest_points = sorted(range(len(cosine_similarities)), key=lambda i: cosine_similarities[i], reverse=True)[:5]

print(closest_points)
for i in closest_points:
  print(res[i][0])
  print('\n\n\n')
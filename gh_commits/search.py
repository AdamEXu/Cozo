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
  "code": "@@ -67,6 +67,8 @@ export const handleDocumentAnalyze = async (\n  const verifiedResponse = verifyResponseOfSubmit(response);\n  if (!verifiedResponse || !verifiedResponse.results) {\n    if (!suppressRateLimitErrors) {\n+      vscode.window.showErrorMessage(CONSTANTS.analyzeCommandTimeoutMessage);\n+    }\n    getExtensionEventEmitter().fire({\n      type: 'Analysis_Error',\n      data: '',\n@@ -77,8 +79,6 @@ export const handleDocumentAnalyze = async (\n        name: currentWorkSpaceFolder,\n      },\n    });\n-      vscode.window.showErrorMessage(CONSTANTS.analyzeCommandTimeoutMessage);\n-    }\n\n    return failedResponseReturn;\n  } else if (verifiedResponse.status === 'failed') {\n@@ -121,7 +121,20 @@ export const handleDocumentAnalyze = async (\n\n  // convert problem paths to absolute path and normalize them\n  const workspaceFolderPath = vscode.workspace.workspaceFolders?.[0].uri.fsPath;\n-  if (!workspaceFolderPath) {return failedResponseReturn;}\n+  if (!workspaceFolderPath) {\n+    getExtensionEventEmitter().fire({\n+      type: 'Analysis_Error',\n+      data: '',\n+    });\n+    getExtensionEventEmitter().fire({\n+      type: 'CURRENT_PROJECT',\n+      data: {\n+        name: currentWorkSpaceFolder,\n+      },\n+    });\n+\n+    return failedResponseReturn;\n+  }\n  verifiedResponse.results.forEach(result => {\n    result.path = path.join(workspaceFolderPath, result.path);\n  });",
  "repo": "MetabobProject/metabob-vscode",
  "commit_id": "f2fc157",
  "file": "ext-src/helpers/HandleDocumentAnalyze.ts",
  "commit_message": "fix analyze button remains disabled when analyze fails",
  "explanation": "Description: Fixes the issue where the analyze button remained disabled after a failed analysis.\nReason: To ensure that the analyze button is re-enabled and the user is notified of the analysis failure.\nChanges: Added error message notifications and event triggers to handle analysis errors and re-enable the analyze button.\nImpact: Improves the user experience by providing feedback on analysis failures and allowing users to re-trigger the analysis process."
}


client = Client('sqlite', 'explanations.db')

# insert new code
script = """
?[code, code_embedding, commit_message, llm_explanation] <- """ + str([[new_code['code'], embedding(new_code['code']), new_code['commit_message'], new_code['explanation']]]) + """
"""

try:
  res = client.run(script)
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

script = """
?[code] := ~gh_explanations:index{ code, code_embedding, commit_message, llm_explanation |
      query: q,
      k: 5,
      ef: 10,
      radius: 0.5
  }, q = vec(""" + str(embedding(new_code['code'])) + """)
"""

try:
  res = client.run(script)
except Exception as e:
  print(f"An error occurred: {e}")

print(res)
client.close()

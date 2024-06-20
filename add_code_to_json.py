print("Paste code and press Ctrl-D to finish.")
contents = []
while True:
  try: 
    line = input()
  except EOFError:
    break
  contents.append(line)

code = "\n".join(contents)

from generation import generate_explanation
explanation = generate_explanation(code)

import json
data = {
  "code": code,
  "explanation": explanation
}

# ADD it to the JSON file (do not replace, only add it to the list)

with open('code.json', 'r') as f:
  datalist = json.load(f)

datalist.append(data)

with open('code.json', 'w') as f:
  json.dump(datalist, f, indent=2)
from openai import OpenAI
client = OpenAI()

def generate_explanation(code):
  system = '''
Generate an explanation for the code change in the following format:
1. General Description: Brief summary on what this change does
2. Reason for the Change: Reason on why the change was done
3. Description of the Change: Description on what changes were made to the code
4. What was done in the Change: What was specifically done in the code
5. Importance of the Change: Importance of the change in the code

In total you should have five lines lines. Do not use markdown formatting, lists, or anything else that could potentially bring the total number of lines above five. You should use plain English. You will receive the code from the user, please follow the instructions and only provide the summary. Please do not double space or add any extra lines. Do not provide any other context or information, just the five lines.
'''

  grounding_code = '''
def sum_two_numbers_efficient(a, b):
    if a == 0:
        return b
    elif b == 0:
        return a
    else:
        return a + b
'''
  grounding_exp = '''
1. General Description: This change optimizes the function sum_two_numbers_efficient to handle cases where either input is zero efficiently.
2. Reason for the Change: Improve performance and readability by reducing unnecessary operations.
3. Description of the Change: Added conditional checks to directly return b when a is zero or return a when b is zero.
4. What was done in the Change: Modified the function to handle zero inputs more efficiently by adding conditional checks.
5. Importance of the Change: Enhances efficiency and clarity, ensuring the function handles zero inputs swiftly.
'''

  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": system},
      {"role": "user", "content": grounding_code},
      {"role": "assistant", "content": grounding_exp},
      {"role": "user", "content": code}
    ],
    logit_bias={"1734": -10, "198": -10}
  )
  if response.choices:
    return response.choices[0].message.content
  else:
    return None  # or any other appropriate default value


if __name__ == "__main__":
  print("Paste code and press Ctrl-D to finish.")
  contents = []
  while True:
    try: 
      line = input()
    except EOFError:
      break
    contents.append(line)

  code = "\n".join(contents)

  explanation = generate_explanation(code)

  print(explanation)

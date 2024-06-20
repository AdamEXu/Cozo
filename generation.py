from openai import OpenAI
client = OpenAI()

def generate_explanation(code):
  system = '''
Generate an explanation for the code change in the following format:
Description: Brief summary on what this change does
Reason: Reason on why the change was done
Changes: Description on what changes were made to the code
Impact: Why is this code change important?

In total you should have four lines. Do not use markdown formatting, lists, or anything else that could potentially bring the total number of lines above 4. You should use plain English. You will receive the code from the user, please follow the instructions and only provide the summary. Please do not double space or add any extra lines. You should only provide the summary.
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
Description: This change optimizes the function sum_two_numbers_efficient to handle cases where either input is zero efficiently.
Reason: Improve performance and readability by reducing unnecessary operations.
Changes: Added conditional checks to directly return b when a is zero or return a when b is zero.
Impact: Enhances efficiency and clarity, ensuring the function handles zero inputs swiftly.
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
  return response.choices[0].message.content

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

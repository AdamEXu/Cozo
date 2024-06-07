# import the client
from pycozo.client import Client

# create a client
client = Client()

# can add comments at the end of the line. this is not implemented in the parser, but i am stripping them out before sending to the parser
# script = """
# a[x, y] <- [[1, 2], [3, 4]]
# b[y, z] <- [[2, 3], [2, 4]]
# """

script = """
code[id, code] <- [[1, 'print()'], [2, 'input()'], [3, 'x = 5']]
explanation[id, explanation] <- [[1, 'prints a new line'], [2, 'takes input from user'], [3, 'assigns 5 to x']]

?[code_snippet, description] := code[id, code_snippet], explanation[id, description]
"""

# temporary variable to store the script
sc = ''

# remove comments
for line in script.split('\n'):
  sc += line.split('#')[0] + '\n'

# remove leading and trailing whitespaces/newlines
sc = sc.strip()

# execute the script
res = None
try:
  res = client.run(sc)
except Exception as e:
  res = None
  raise(e)
finally:
  client.close()

# print the result
if 'res' in locals() and res is not None:
  print(res)
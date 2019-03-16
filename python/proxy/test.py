import json
list = [{'erew': 9}, (3, 4)] # Note that the 3rd element is a tuple (3, 4)
t = json.dumps(list) # '[1, 2, [3, 4]]'
print t
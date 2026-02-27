import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

text = "Hey There! My name is Hamza Ahmad"
tokens = enc.encode(text)

print("Tokens: ", tokens) # Tokens:  [25216, 3274, 0, 3673, 1308, 382, 20665, 2051, 97625]

decoded = enc.decode([25216, 3274, 0, 3673, 1308, 1994, 20665, 2051, 97625])
print("Decoded: ", decoded) # Decoded:  Hey There! My name is Hamza Ahmad
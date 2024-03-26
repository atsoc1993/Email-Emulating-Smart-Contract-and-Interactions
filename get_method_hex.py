from algosdk.abi import Method

signature1 = "set_owner()void" #2867b803
signature2 = "message()void" #f00ec344

print(Method.from_signature(signature1).get_selector().hex())
print(Method.from_signature(signature2).get_selector().hex())


import base64

string = "fYZ7ipGIjFtsXpNLbHdPbXdaam1PS1c5lQ=="
decoded = base64.b64decode(string)
print(decoded)

for shift in range (256):
    new = ""
    for i in decoded:
        new += chr((ord(i)-shift)%256)
    print("{} : {}".format(shift,new))
import sys
from pycape import Cape

if len(sys.argv) < 2:
    print("expected user to be passed")
    quit()

cape = Cape()

ciphertext = cape.encrypt(f"hi {sys.argv[1]}".encode(), username=sys.argv[1])

print("Encrypted:", ciphertext.decode())

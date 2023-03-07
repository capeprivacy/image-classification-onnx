from pycape import Cape

cape = Cape()

ciphertext = cape.encrypt(b"hello world")

print("Encrypted:", ciphertext.decode())


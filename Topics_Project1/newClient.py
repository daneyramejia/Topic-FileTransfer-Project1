class Encryptor():

    def key_create(self):
        key = Fernet.generate_key()
        return key

    def key_write(self, key, key_name):
        with open(key_name, 'wb') as mykey:
            mykey.write(key)

    def key_load(self, key_name):
        with open(key_name, 'rb') as mykey:
            key = mykey.read()
        return key


    def file_encrypt(self, key, original_file, encrypted_file):
        
        f = Fernet(key)

        with open(original_file, 'rb') as file:
            original = file.read()

        encrypted = f.encrypt(original)

        with open (encrypted_file, 'wb') as file:
            file.write(encrypted)

    def file_decrypt(self, key, encrypted_file, decrypted_file):
        
        f = Fernet(key)

        with open(encrypted_file, 'rb') as file:
            encrypted = file.read()

        decrypted = f.decrypt(encrypted)

        with open(decrypted_file, 'wb') as file:
            file.write(decrypted)


import socket

HOST = socket.gethostbyname(socket.gethostname())
PORT = 4455
ADDR = (HOST, PORT)
FORMAT = "utf-8"
SIZE = 1024

def main():
    #starting socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #attempting connection
    client.connect(ADDR)

    #opening and reading
    file = open("yt.txt", "r")
    data = file.read()

    #filename --> server
    client.send("yt.txt".encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")

    #file data --> server
    client.send(data.encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")

    #closing file
    file.close()

    #closing connection
    client.close()


if __name__ == "__main__":
    main()

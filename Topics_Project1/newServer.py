from cryptography.fernet import Fernet

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

#start of TCP socketing and file transfer     
import socket

HOST = socket.gethostbyname(socket.gethostname())
PORT = 4455
ADDR = (HOST, PORT)
SIZE = 1024
FORMAT = "utf-8"

def main():
    print("[STARTING] Server is starting.")
    #starting the tcp socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #binding the host and port into address
    server.bind(ADDR)

    #server is beginning to listen
    server.listen()
    print("[LISTENING] Server is listening.")

    encryptor = Encryptor()
    mykey = encryptor.key_create()
    encryptor.key_write(mykey, 'mykey.key')
    loaded_key = encryptor.key_load('mykey.key')
    encryptor.file_encrypt(loaded_key, 'yt.txt', 'enc_yt.txt')
    encryptor.file_decrypt(loaded_key, 'enc_yt.txt', 'dec_yt.txt')

    while True:
        #accepting the connection
        conn, addr = server.accept()
        print(f"[NEW CONNECTION] {addr} connected.")

        #getting filename from client
        filename = conn.recv(SIZE).decode(FORMAT)
        print(f"[RECV] Receiving the filename.")
        file = open(filename, "w")
        conn.send("Filename received.".encode(FORMAT))

        #getting file data from client
        data = conn.recv(SIZE).decode(FORMAT)
        print(f"[RECV] Receiving the file data.")
        file.write(data)
        conn.send("File data received".encode(FORMAT))

        #closing the file
        file.close()

        #closing the connection
        conn.close()
        print(f"[DISCONNECTED] {addr} disconnected.")

if __name__ == "__main__":
    main()


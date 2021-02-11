################################################### IMPORT #############################################################

import os
import socket

###################################################### KONEKSI #########################################################

s = socket.socket()
host = "127.0.0.1"
port = 2432

def koneksi():
    try:
        s.connect((host,port))
    except:
        print("Server belum diaktifkan")
        koneksi()
    else:
        passwd = s.recv(1024).decode()
        try:
            while True:
                teb = input("Masukkan kode aktivasi dari server\n>>> ")
                if passwd==teb:
                    status = "1".encode()
                    s.send(status)
                    print("Berhasil Terhubung Dengan Server")
                    break
        except:
            quit()
koneksi()

################################################### LOGIKA #############################################################

while True:
    command = s.recv(1024).decode()

    if command == "listdir":
        try:
            lokasi = s.recv(1024).decode()
            dir = str(os.listdir(lokasi))
        except:
            fail = s.send("fail".encode())
        else:
            fail = s.send("success".encode())
            apa = dir.replace("[","")
            apa = apa.replace("]","")
            s.send(apa.encode())


    if command == "shutdown":
        try:
            timer = int(s.recv(1024).decode())
            os.system(f"shutdown /s /t {timer}")
        except:
            continue


    if command == "removefile":
        try:
            lokasi = s.recv(1024).decode()
            os.remove(lokasi)
        except:
            fail = s.send("fail".encode())
        else:
            fail = s.send("success".encode())

    if command == "download":
        try:
            lokasi = s.recv(1024).decode()
            file = open(lokasi, "rb")
            data = file.read()
        except:
            fail = s.send("fail".encode())
        else:
            faill = s.send("success".encode())
            s.send(data)

    if command == "send":
        kondisi = s.recv(1024).decode()
        if kondisi=="gagal":
            continue
        if kondisi=="berhasil":

            file = s.recv(90000000)
            lokasi = open(f"C:/untitled", "wb")
            lokasi.write(file)

    if command == "off":
        quit()
########################################################################################################################

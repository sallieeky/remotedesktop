####################################################### IMPORT #########################################################

from tkinter import *
from tkinter import messagebox

import socket
import threading
import time, datetime
import random
import string

############################################################## ROOT ####################################################

root = Tk()
root.wm_title("Tubes Kelompok 2 H")
root.geometry("600x550")
root.wm_iconbitmap("folderremote_103599.ico")

passwd = ""
count = 0

def generate():
    global passwd
    passwd = ""
    for i in range(8):
        ran = random.choice(string.ascii_letters)
        passwd += ran
    return passwd

########################################################### KONEKSI ####################################################

def aktivitas():
    asda = datetime.datetime
    with open("log.txt", "w") as f:
        name = socket.gethostname()
        f.write(f"AKTIVITAS TERAKHIR SERVER\n"
                f"Time : {asda.now()}\n"
                f"Hostname : {name}")

def konek():
    global count, hostname, conn, s
    count+=1
    if count%2==1:
        home_f()
        generate()
        status = "0"
        connect["command"] = threading.Thread(target=konek).start
        client_l["text"] = "Waiting Client"
        format_log("Server Has Been Started")
        connect["text"] = "DISCONNECT"
        format_log(f"Kode aktivasi untuk client : {passwd}")
        while status == "0":
           try:
                s = socket.socket()
                host = "127.0.0.1"
                port = 2432
                s.bind((host,port))
                s.listen(1)
                aktivitas()
                conn, addr = s.accept()
                conn.send(passwd.encode())
                status = conn.recv(1024).decode()
           except:
               count+=1
        format_log("Client Has Been Connected")
        client_l["text"] = f"Client Has Been Connected\n{addr[0]}, {addr[1]}"
        radio_status("normal")

    elif count%2==0:
        command = "off".encode()
        conn.send(command)
        s.close()
        home_f()
        connect["command"] = threading.Thread(target=konek).start
        client_l["text"] = "Start the Server"
        format_log("Server diberhentikan")
        home.select()
        radio_status("disabled")
        connect["text"] = "CONNECT"
        basic["text"] = "\tSTART THE SERVER\n\tCLICK CONNECT BUTTON"

#################################################### FUNGSI TOMBOL #####################################################

def listdir_f():
    command = "listdir".encode()
    conn.send(command)
    lokasi = directory_location.get()
    conn.send(lokasi.encode())
    fail = conn.recv(1024).decode()
    directory_b["command"] = threading.Thread(target=listdir_f).start
    if "D:/" not in lokasi and "C:/" not in lokasi and "E:/" not in lokasi and "F:/" not in lokasi and "G:/" not in lokasi:
        format_log("Masukkan inputan dengan benar")
    else:
        if fail == "fail":
            format_log("Directory tidak ditemukan")
        else:
            conn.send(lokasi.encode())
            dir = conn.recv(5000).decode()
            format_log(lokasi+" : "+dir)

def shutdown_f():
    command = "shutdown".encode()
    conn.send(command)
    e = time_e.get()
    shutdown_b["command"] = threading.Thread(target=shutdown_f).start
    if e.isdigit() == True:
        conn.send(e.encode())
        format_log("Perintah shutdown berhasil dieksekusi")
    else:
        messagebox.showinfo("Masukan Tidak Valid", "Masukan Waktu Dalam Bentuk Angka")
        time_e.delete(0,END)
        format_log("Perintah Shutdown Tidak Valid (masukkan waktu dalam bentuk angka)")
        conn.send(e.encode())

def removefile_f():
    command = "removefile".encode()
    conn.send(command)

    lokasi = directoryre_location.get()
    conn.send(lokasi.encode())
    fail = conn.recv(1024).decode()
    directoryr_b["command"] = threading.Thread(target=removefile_f).start
    if fail == "fail":
        format_log("File tidak ditemukan")
    else:
        format_log("File berhasil di hapus dari directory")

def download_file_f():
    command = "download".encode()
    conn.send(command)
    nama = ""

    lokasi = directorydown_location.get()
    conn.send(lokasi.encode())
    fail = conn.recv(1024).decode()
    directorydown_b["command"] = threading.Thread(target=download_file_f).start
    if fail == "fail":
        format_log("File tidak ditemukan")
    else:
        lok = str(lokasi).split("/")
        for i in range(len(lok)):
            if "." in lok[i]:
                nama+=lok[i]
        file = conn.recv(900000000)
        letak = open(f"C:/{nama}", "wb")
        letak.write(file)
        letak.close()
        format_log(f"File Berhasil Didownload\nLokasi Penyimpanan >>> D:/Alpro Python/TUBES/remote GUI/Tes/Download Tes/{nama}")

def send_file_f():
    command = "send".encode()
    conn.send(command)
    directorysend_b["command"] = threading.Thread(target=send_file_f).start
    lokasi = directorysend_location.get()
    try:
        file = open(lokasi, "rb")
        data = file.read()
    except:
        format_log("File tidak ditemukan")
        conn.send("gagal".encode())
    else:
        conn.send("berhasil".encode())
        conn.send(data)
        format_log("File berhasil dikirim ke client")

################################################### FUNGSI TAMPILAN ####################################################

def radio_status(kondisi):
    home.config(state=kondisi)
    listdir.config(state=kondisi)
    shutdown.config(state=kondisi)
    remove_file.config(state=kondisi)
    download_file.config(state=kondisi)
    send_File.config(state=kondisi)

def descre():
    global left_frame
    left_frame.destroy()
    left_frame = Frame(root)
    left_frame.pack(side=LEFT, fill=X)

def format_log(message):
    log.config(state="normal")
    log.insert(INSERT, "\n"+time.strftime("%H:%M:%S ")+message+"\n")
    log.config(state="disabled")

def home_f():
    global basic
    descre()
    basic = Label(left_frame, text="\tSERVER HAS BEEN STARTED", font=("arial",14))
    basic.grid()
    basic.pack()

def listdir_option_f():
    global directory_location, directory_b
    descre()

    sub_l = Label(left_frame, text="VIEW DIRECTORY LIST", font=("arial",14))
    sub_l.grid(pady=10)

    directory_l = Label(left_frame, text="Masukkan Lokasi Directory")
    directory_l.grid(padx=10)
    directory_location = Entry(left_frame, font=("arial",10), width=50, justify=CENTER)
    directory_location.grid(padx=10)

    directory_b = Button(left_frame, text="LIHAT ISI DIRECTORY", command = threading.Thread(target=listdir_f).start)
    directory_b.grid(pady=10)

def shutdown_option_f():
    global time_e, shutdown_b
    descre()
    sub_l = Label(left_frame, text="\tSHUTDOWN OPTION\t", font=("arial",14))
    sub_l.grid(pady=10)

    time_l = Label(left_frame, text="Timer")
    time_l.grid(padx=10)
    time_e = Entry(left_frame, font=("arial",10), width=50, justify=CENTER)
    time_e.grid(padx=10)

    shutdown_b = Button(left_frame, text="SHUTDOWN", command=threading.Thread(target=shutdown_f).start)
    shutdown_b.grid(pady=10)


def removefile_option_f():
    global directoryre_location, directoryr_b
    descre()

    sub_l = Label(left_frame, text="REMOVE FILE IN DIRECTORY", font=("arial",14))
    sub_l.grid(pady=10)

    directory_l = Label(left_frame, text="Masukkan Lokasi Directory")
    directory_l.grid(padx=10)
    directoryre_location = Entry(left_frame, font=("arial",10), width=50, justify=CENTER)
    directoryre_location.grid(padx=10)

    directoryr_b = Button(left_frame, text="REMOVE FILE", command=threading.Thread(target=removefile_f).start)
    directoryr_b.grid(pady=10)


def download_file_option_f():
    global directorydown_location, directorydown_b
    descre()
    sub_l = Label(left_frame, text="DOWNLOAD FILE CLIENT", font=("arial",14))
    sub_l.grid(pady=10)

    directory_l = Label(left_frame, text="Masukkan Lokasi Directory")
    directory_l.grid(padx=10)
    directorydown_location = Entry(left_frame, font=("arial",10), width=50, justify=CENTER)
    directorydown_location.grid(padx=10)

    directorydown_b = Button(left_frame, text="DOWNLOAD FILE", command=threading.Thread(target=download_file_f).start)
    directorydown_b.grid(pady=10)

def send_file_option_f():
    global directorysend_location, directorysend_b
    descre()
    sub_l = Label(left_frame, text="SEND FILE TO CLIENT", font=("arial",14))
    sub_l.grid(pady=10)

    directory_l = Label(left_frame, text="Masukkan Lokasi Directory")
    directory_l.grid(padx=10)
    directorysend_location = Entry(left_frame, font=("arial",10), width=50, justify=CENTER)
    directorysend_location.grid(padx=10)

    directorysend_b = Button(left_frame, text="SEND FILE", command=threading.Thread(target=send_file_f).start)
    directorysend_b.grid(pady=10)


#################################################### FRAME #############################################################

bottom_frame = Frame(root)
bottom_frame.pack(side=BOTTOM)

root_frame = Frame(root)
root_frame.pack(side=TOP, fill=BOTH)

right_frame = Frame(root)
right_frame.pack(side=RIGHT, fill=Y)

left_frame = Frame(root)
left_frame.pack(side=LEFT, fill=X)

########################################################### LABEL ######################################################

judul_l = Label(root_frame, text="Program Remote Computer", font=("arial", 12))
judul_l.grid(pady=10)
judul_l.pack()

basic_l = Label(left_frame, text="\tSTART THE SERVER\n\tCLICK CONNECT BUTTON", font=("arial",14))
basic_l.grid()
basic_l.pack()


info_l = Label(right_frame, text="Control Panel", font=("arial", 12))
info_l.grid(row=0, column=0)

client_l = Label(right_frame, text="Start the Server", font=("arial", 10))
client_l.grid(pady=10, padx=10)

######################################################## BUTTON ########################################################

connect = Button(bottom_frame, text="CONNECT", command=threading.Thread(target=konek).start)
connect.grid(pady=10)

######################################################## RADIO #########################################################

home = Radiobutton(right_frame, text="Home\t\t\t", value=0, command=home_f)
listdir = Radiobutton(right_frame, text="Lihat Isi Directory", value=1, command=listdir_option_f)
shutdown = Radiobutton(right_frame, text="Shutdown", value=2, command=shutdown_option_f)
remove_file = Radiobutton(right_frame, text="Remove File", value=4, command=removefile_option_f)
download_file = Radiobutton(right_frame, text="Download File", value=6, command=download_file_option_f)
send_File = Radiobutton(right_frame, text="Send File", value=7, command=send_file_option_f)

radio_status("disabled")

home.grid(sticky=W, padx=10, pady=5)
listdir.grid(sticky=W, padx=10, pady=5)
shutdown.grid(sticky=W, padx=10, pady=5)
remove_file.grid(sticky=W, padx=10, pady=5)
download_file.grid(sticky=W, padx=10, pady=5)
send_File.grid(sticky=W, padx=10, pady=5)

home.select()

######################################################## TEKSBOX #######################################################

log = Text(bottom_frame, font=("arial", 10), height=10, width=83, bd=5)
log.grid(row=1)
log.insert(INSERT, "========================= WELCOME TO THE SERVER ========================\n")
log.config(state="disabled")

########################################################################################################################

root.mainloop()

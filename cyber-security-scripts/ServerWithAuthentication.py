import socket,hashlib,threading
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostbyname(socket.gethostname())
port = 1234
s.bind((host,port))
ip_list = []
conn_list = []
logged_in_users = []
print(f"\n[+] Server hosted on IP: {host}")
print(f"[+] Server hosted on Port: {port}")
print("\n[+] Server is Up And Running.........\n")
try:
    checker = open('username_passwords.txt', 'r')
except:
    checker = open('username_passwords.txt','w')
def listener():
    while True:
        try:
            s.listen(1)
            conn, ip = s.accept()
            if ip[0] in ip_list:
                message = "You cannot have more than 1 session at a time!".encode('utf-8')
                conn.send(message)
                conn.close()
            else:
                msg = f"\n[+] {ip[0]} Has Joined the Server.\n"
                print(msg)
                reciever = threading.Thread(target=recv,args=(conn, ip[0]))
                reciever.start()
            ip_list.append(ip[0])
            conn_list.append(conn)
        except:
            pass
def recv(connections, ips):
    logged = False
    while True:
        try:
            msg = connections.recv(1024)
            msg = msg.decode()
            if logged:
                msg_split = msg.split()
                user = msg_split[0]
                del msg_split[0]
                main_msg = ""
                for i in msg_split:
                    main_msg = main_msg + " " + i
                msg = main_msg.strip()
            elif not logged:
                pass
            if msg.strip() == "":
                pass
            else:
                try:
                    print(f"[({user})]: {msg}")
                except:
                    print(f"[({ips})]: {msg}")
                if not logged:
                    if msg.startswith('!login'):
                        file = open("username_passwords.txt", 'r')
                        msg = msg.split()
                        try:
                            username = msg[1]
                            password = msg[2]
                        except:
                            error_msg = 'Invalid Arguements!\nUsage: !login <username> <password>'.encode('utf-8')
                            connections.send(error_msg)
                        file_contents = file.readlines()
                        file.close()
                        flag = 0
                        for line in file_contents:
                            if username in line:
                                info = line
                                flag = 1
                                break
                            else:
                                pass
                        if flag == 0:
                            error_msg = 'Your Username Does Not Exist! Try Registering.'.encode('utf-8')
                            connections.send(error_msg)
                        else:
                            info = info.split()
                            passw = info[1]
                            hashed_pass = hashlib.md5(password.encode()).hexdigest()
                            if passw.strip() == hashed_pass.strip():
                                msg = f'Password Accepted! Welcome {username}.'.encode('utf-8')
                                connections.send(msg)
                                message = f"{username} Has Joined the Server!"
                                msgtoclient = "\n[+] List Of Commands:\n\n[+] !send <username> <msg> - Sends a direct message to the username specified.\n[+] !broadcast <msg> - Sends a message to all clients\n[+] !login <username> <password> - This is for users not using the official client side script.\n[+] !register <username> <password> - This is also for users not using the official client side script.\n[+] !reregister <username> <old_password> <new_password> - Change your password.\n!listusers - Lists all connected Users.\n".encode(
                                    'utf-8')
                                connections.send(msgtoclient)
                                for client in conn_list:
                                    try:
                                        if client == connections:
                                            pass
                                        else:
                                            client.send(message.encode('utf-8'))
                                    except:
                                        pass
                                logged = True
                                listitem = f"{username} {ips}"
                                logged_in_users.append(listitem)
                            else:
                                if flag == 1:
                                    error_msg = 'Password Not Accepted!'.encode('utf-8')
                                    connections.send(error_msg)
                                else:
                                    pass
                    elif msg.startswith('!register'):
                        stop = False
                        msg = msg.split()
                        flag = 0
                        try:
                            new_user = msg[1]
                            new_pass = msg[2]
                            flag = 1
                        except:
                            error_msg = 'Invalid Arguements!\nUsage: !register <username> <password>'.encode('utf-8')
                            connections.send(error_msg)
                        file = open("username_passwords.txt", 'r')
                        file_contents = file.readlines()
                        file.close()
                        for line in file_contents:
                            if new_user in line:
                                error_msg = 'The Username is taken! Try using another.'.encode()
                                connections.send(error_msg)
                                stop = True
                                break
                            else:
                                pass
                        if not stop:
                            file = open("username_passwords.txt", "w")
                            new_pass = hashlib.md5(new_pass.encode()).hexdigest()
                            file_contents.extend(f'\n{new_user} {new_pass}')
                            file.writelines(file_contents)
                            file.close()
                            if flag == 1:
                                msg = f"Successfully registered. Welcome, {new_user}!".encode('utf-8')
                                connections.send(msg)
                if logged:
                    if msg.startswith('!broadcast'):
                        msg = msg.split()
                        del msg[0]
                        message = ""
                        for i in msg:
                            message = message + " " + i
                        message = f"\n[({user})]: {message.strip()}"
                        msgtoclient = "Successfully Broadcasted Your Message to the other users.".encode('utf-8')
                        for person in conn_list:
                            try:
                                if person == connections:
                                    pass
                                else:
                                    person.send(message.encode('utf-8'))
                            except:
                                pass
                        connections.send(msgtoclient)
                    elif msg.startswith('!reregister'):
                        flag = 0
                        msg = msg.split()
                        try:
                            username = msg[1]
                            old_pass = msg[2]
                            new_pass = msg[3]
                        except:
                            error_msg = 'Invalid Arguements!\nUsage: !register <username> <old_password> <new_password>'.encode(
                                'utf-8')
                            connections.send(error_msg)
                        file = open('username_passwords.txt', 'r')
                        file_contents = file.readlines()
                        file.close()
                        item = 0
                        for line in file_contents:
                            if username in line:
                                info = line
                                break
                            else:
                                pass
                            item += 1
                        info = info.split()
                        password = info[1]
                        old_pass = hashlib.md5(old_pass.encode()).hexdigest()
                        if old_pass == password:
                            flag = 1
                        else:
                            flag = 0
                        if flag == 1:
                            password = new_pass
                            new_pass = hashlib.md5(new_pass.encode()).hexdigest()
                            file_contents.remove(file_contents[item])
                            file_contents.extend(f'\n{username} {new_pass}')
                            file.close()
                            file = open('username_passwords.txt', 'w')
                            file.writelines(file_contents)
                            msg = f'Hello {username}, you have changed your password to: {password}'.encode()
                            connections.send(msg)
                    elif msg.startswith('!send'):
                        flag = 0
                        msg = msg.split()
                        tar_ip = msg[1]
                        sent_person = msg[1]
                        del msg[0]
                        del msg[0]
                        message = ""
                        for i in msg:
                            message = message + " " + i
                        for i in logged_in_users:
                            if str(tar_ip) in i:
                                ip = i.split()
                                tar_ip = ip[1]
                                break
                            else:
                                pass
                        for connection in conn_list:
                            person = connection
                            if tar_ip in str(person):
                                message = f'\n[+] DM From {user}: {message.strip()}'.encode('utf-8')
                                person.send(message)
                                flag = 1
                            else:
                                pass
                        if flag == 1:
                            msg = f'Successfully sent message to {sent_person}'.encode('utf-8')
                            connections.send(msg)
                        else:
                            msg = f'There was an error with sending the message to {sent_person}'.encode('utf-8')
                            connections.send(msg)
                    elif msg.startswith('!listusers'):
                        users = []
                        for i in logged_in_users:
                            user = i.split()
                            user = user[0]
                            users.append(user)
                        msgtoclient = ""
                        for i in users:
                            msgtoclient = msgtoclient + " " + i
                        msgtoclient = msgtoclient.strip()
                        connections.send(msgtoclient.encode('utf-8'))
                    else:
                        pass
        except:
            pass
def send():
    while True:
        msg = input("[+] Enter your message: ")
        msg = f"\n[(SERVER)]: {msg}"
        for item in conn_list:
            try:
                item.send(msg.encode('utf-8'))
            except:
                pass
def conn_checker():
    while True:
        for conn in conn_list:
            try:
                msg = "".encode('utf=8')
                conn.send(msg)
            except:
                item = 0
                for ip in ip_list:
                    if ip in str(conn):
                        print(f"\n[+] {ip} Is Offline.\n")
                        ip_list.remove(ip_list[item])
                        conn.close()
                    else:
                        pass
                    item += 1
listen = threading.Thread(target=listener)
listen.start()
handler = threading.Thread(target=conn_checker)
handler.start()
sender = threading.Thread(target=send)
sender.start()

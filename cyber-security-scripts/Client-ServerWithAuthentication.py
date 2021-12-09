import socket, threading, sys
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        ip = input("[+] Enter the IP to connect to: ")
        port = int(input("[+] Enter the Port to connect to: "))
        s.connect((ip, port))
        break
    except:
        print("\n[+] Invalid IP or Port.\n")
commands_list = ['!reregister','!send','!broadcast','!listusers']
print("[+] Connected to the server.......\n")
login = False
register = True
def instruct():
    while True:
        try:
            global register
            global login
            if register:
                while True:
                    register_q = input("[+] Do you wish to register for a new account?(yes/no): ")
                    if register_q.lower() == "yes":
                        print("[+] You are going to register.\n")
                        new_user = input("[+] Enter your username: ")
                        new_pass = input("[+] Enter your password: ")
                        msg = f"!register {new_user} {new_pass}".encode()
                        s.send(msg)
                        servmsg = s.recv(1024).decode()
                        if "Successfully registered." in servmsg:
                            print("[+] You have been registered!")
                            register = False
                            break
                        elif "The Username is taken!" in servmsg:
                            print("[+] The Username has been taken. Try using another.\n")
                    elif register_q.lower() == "no":
                        register = False
                        break
                    else:
                        print("[+] Please answer with either 'yes' or 'no'.")
            if not login:
                print("\n[+] You are required to login.\n")
                username = input("[+] Enter your username: ")
                password = input("[+] Enter your password: ")
                msg = f"!login {username} {password}".encode('utf-8')
                s.send(msg)
                servmsg = s.recv(1024).decode()
                if "Password Accepted!" in servmsg:
                    login = True
                    print(f"\n[+] Successfully logged in as: {username}\n")
                    reciever = threading.Thread(target=recv)
                    reciever.start()
                elif "Password Not Accepted!" in servmsg:
                    login = False
                    print("[+] The password you provided is invalid.")
                elif "Your Username Does Not Exist" in servmsg:
                    print("[+] The username you provided is invalid. Try to register.\n")
                    register = True
            elif login:
                instruction = input("[+] What is the instruction: ")
                try:
                    insplit = instruction.split()
                    instruction = f"{username} {instruction}"
                    if insplit[0] in commands_list:
                        try:
                            s.send(instruction.encode('utf-8'))
                        except:
                            print("[+] Your Connection has been Terminated by the host.")
                            input("\n[+] Press 'enter' to exit.")
                            s.close()
                            sys.exit()
                except:
                    print("\n[+] Your message is invalid!")
        except:
            pass
def recv():
    while True:
        try:
            msg = s.recv(1024)
            msg = msg.decode('utf-8')
            if msg == "":
                pass
            else:
                print(f"\n[+] Msg from Serv: {msg}")
        except:
            pass
sender = threading.Thread(target=instruct)
sender.start()

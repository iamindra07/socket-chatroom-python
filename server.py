import socket
import threading
import datetime
import re
# import ollama
from google import genai
import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()
ai = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# agent = ollama.Client()

# model = "llama2"
# # prompt = input("Enter your prompt: ")
# # response = client.generate(model=model, prompt=prompt)
# # print(response.response)
IP = "127.0.0.1"
PORT = 12345
ADDR = (IP,PORT)
Clients = []
Names = []

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind(ADDR)
server_socket.listen()
print("[SERVER IS LISTENING ...]")

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def broadcast(client_socket,msg):
    msg = f'[{Colors.BLUE}{str(datetime.datetime.now().strftime("%H:%M:%S"))}{Colors.RESET}] {msg}'
    msg = msg.encode('utf-8')
    for client in Clients:
        if(client == client_socket):
            continue
        client.send(msg)

def handle(client):
    while True:
        try:
            msg = client.recv(4096).decode('utf-8')
            msg = msg.replace("\n", " ")
            index = Clients.index(client)
            name = Names[index]
            if msg ==  f"/help":
                text = f"""{Colors.BLUE}
---> TO SEE WHO IS ONLINE USE '/online'
---> TO ASK AI A QUESTION USE '/ai'
        EXAMPLE ==> /ai what is the capital of france ?
---> TO SEND TEXT IN DFFERENT COLOR USE '/red','/green','/blue'
        EXAMPLE ==> /red hello
--->TO QUIT THE CHAT USE '/quit'
--->TO REPLY TO SOMEONE USE '@' 
        EXAMPLE ==> @username:message
--->TO PRIVATELY REPLY TO SOMEONE USE'p@'
        EXAMPLE ==> p@username:message
--->TO CHANGE COLOR OF YOUR NAME to Red, green or blue use
                '/setcR' , '/setcG' , '/setcG'
        TO RESET COLOR USE '/resetc'{Colors.RESET}  
                """
                client.send(text.encode('utf-8'))
                continue
            if msg == "/setcR":
                name = re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', name)
                Names[index] = f'{Colors.RED}{name}{Colors.RESET}'
                client.send(f'{Colors.RED}THE COLOR OF YOUR NAME HAS BEEN CHANGED TO RED !{Colors.RESET}'.encode('utf-8'))
                continue
            if msg == "/setcG":
                name = re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', name)
                Names[index] = f'{Colors.GREEN}{name}{Colors.RESET}'
                client.send(f'{Colors.GREEN}THE COLOR OF YOUR NAME HAS BEEN CHANGED TO GREEN !{Colors.RESET}'.encode('utf-8'))
                continue
            if msg == "/setcB":
                name = re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', name)
                Names[index] = f'{Colors.BLUE}{name}{Colors.RESET}'
                client.send(f'{Colors.BLUE}THE COLOR OF YOUR NAME HAS BEEN CHANGED TO RED !{Colors.RESET}'.encode('utf-8'))
                continue
            if msg == "/resetc":
                name = re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', name)
                Names[index] = f'{name}'
                client.send('THE COLOR OF YOUR NAME HAS BEEN RESET !'.encode('utf-8'))
                continue
            if msg == "/online":
                lenght = len(Names)
                client.send(f"[{Colors.GREEN}TOTAL ONLINE MEMBERS : {lenght}{Colors.RESET}]".encode('utf-8'))
                for member in Names:
                    client.send(f"{Colors.GREEN}{member}{Colors.RESET}\n".encode('utf-8')) 
                continue  
            if msg.startswith("p@"):
                try:
                    username, text = msg.split(":",1)
                    text = text.strip()
                    username = username.strip()[2:]
                    uindex = Names.index(username)
                    uclient = Clients[uindex]
                    uclient.send(f'[{Colors.BLUE}{str(datetime.datetime.now().strftime("%H:%M:%S"))}{Colors.RESET}] {name} privately replied to you :{text}'.encode('utf-8'))
                except:
                    client.send("Invalid format. Use p@username:message".encode('utf-8'))
                continue
            if msg.startswith("@"):
                try:
                    username , text = msg.split(":",1)
                    text = text.strip()
                    username = username.strip()[1:]
                    uindex = Names.index(username)
                    uclient = Clients[uindex]
                    for member in Clients:
                        if member == uclient:
                            uclient.send(f'[{Colors.BLUE}{str(datetime.datetime.now().strftime("%H:%M:%S"))}{Colors.RESET}] {name} replied to you :{text}'.encode('utf-8'))
                            continue
                        if member == client:
                            continue
                        member.send(f'[{Colors.BLUE}{str(datetime.datetime.now().strftime("%H:%M:%S"))}{Colors.RESET}] {name} replied to {username} :{text}'.encode('utf-8'))
                except:
                    client.send("Invalid format. Use @username:message".encode('utf-8'))
                continue
            if msg.startswith("/red"):
                msg = msg.replace("/red",'')
                msg = msg.strip()
                msg =f"{Colors.RED}{msg}{Colors.RESET}"
            if msg.startswith("/green"):
                msg = msg.replace("/green",'')
                msg = msg.strip()
                msg =f"{Colors.GREEN}{msg}{Colors.RESET}" 
            if msg.startswith("/blue"):
                msg = msg.replace("/blue",'')
                msg = msg.strip()
                msg =f"{Colors.BLUE}{msg}{Colors.RESET}"
            if msg.startswith("/ai"):
                msg = msg.replace("/ai",'')
                msg = msg.strip()
                # response = agent.generate(model=model, prompt=msg)
                # msg =str(response.response)
                response = ai.models.generate_content(
                    model="gemini-3.5-flash",
                    contents=msg
                )
                msg = response.text
                msg = msg.replace("\n", " ")
                msg = f"{Colors.GREEN}AI : {msg}{Colors.RESET}"
                client.send(msg.encode('utf-8'))
                continue
            if msg == "/quit":
                client.close()
                Clients.remove(client)
                Names.remove(name)
                broadcast(client,f"{name} left the chat")
                break
            broadcast(client,f'{name} : {msg}')
        except:
            index = Clients.index(client)
            Clients.remove(client)
            client.close()
            name = Names[index]
            Names.remove(name)
            broadcast(client,f"{name} left the chat")
            break

def receive():
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"[CONNECTED WITH {client_address}]")
        client_socket.send('NAME'.encode('utf-8'))
        name = client_socket.recv(1024).decode('utf-8')
        Names.append(name)
        Clients.append(client_socket)
        print(f"Name of the client is {name}")
        broadcast(client_socket,f"{name} joined the chat")
        client_socket.send("[CONNECTED TO THE SERVER]".encode('utf-8'))
        client_socket.send(f"{Colors.GREEN}USE /help TO SEE ALL COMMANDS{Colors.RESET}".encode('utf-8'))
        thread = threading.Thread(target=handle, args = (client_socket,))
        thread.start()

receive()
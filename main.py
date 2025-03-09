import asyncio
import websockets
import getpass
import pyautogui
import tkinter as tk
from tkinter import messagebox
import secrets

password = None

tokens = ['a2819f48ce87760ea1b5feca7adc727c']
is_dragging = False

async def handle_connection(websocket):
    try:
        async for message in websocket:
            global is_dragging
            print(f"Received: {message}")
            message = message.split('&')
            if message[0].split(':')[0] == "auth":
                root = tk.Tk()
                root.withdraw()
                result = messagebox.askquestion("Connection", "Do you want to connect?").lower()
                if result == 'yes':
                    token = secrets.token_hex(16)
                    tokens.append(token)
                    await websocket.send(f"auth:success&token:{token}")
                else:
                    websocket.send("auth:failed")
                # use tkinter to ask if authorize connection
                # if yes, create token secrets.token_hex(16) and store it in tokens, then send the token
            elif message[0].split(':')[0] == "token" and message[0].split(':')[1] in tokens: # token:<token>&command:<command>
                if message[1].split(':')[0] == "command":
                    command = message[1].split(':')[1]
                    match command:
                        case "mousemoveup":
                            if is_dragging:
                                pyautogui.drag(0,-15,duration=0.1)
                            else:
                                pyautogui.move(0,-15,duration=0.1)
                        case "mousemovedown":
                            if is_dragging:
                                pyautogui.drag(0,15,duration=0.1)
                            else:
                                pyautogui.move(0,15,duration=0.1)
                        case "mousemoveleft":
                            if is_dragging:
                                pyautogui.drag(-15,0,duration=0.1)
                            else:
                                pyautogui.move(-15,0,duration=0.1)
                        case "mousemoveright":
                            if is_dragging:
                                pyautogui.drag(15,0,duration=0.1)
                            else:
                                pyautogui.move(15,0,duration=0.1)
                        case "mousemoveupleft":
                            if is_dragging:
                                pyautogui.drag(-15,-15,duration=0.1)
                            else:
                                pyautogui.move(-15,-15,duration=0.1)
                        case "mousemovedownright":
                            if is_dragging:
                                pyautogui.drag(15,15,duration=0.1)
                            else:
                                pyautogui.move(15,15,duration=0.1)
                        case "mousemovedownleft":
                            if is_dragging:
                                pyautogui.drag(-15,15,duration=0.1)
                            else:
                                pyautogui.move(-15,15,duration=0.1)
                        case "mousemoveupright":
                            if is_dragging:
                                pyautogui.drag(15,-15,duration=0.1)
                            else:
                                pyautogui.move(15,-15,duration=0.1)
                        case "mouseleftclick":
                            pyautogui.mouseDown()
                            pyautogui.mouseUp()
                        case "mouserightclick":
                            pyautogui.mouseDown(button='right')
                            pyautogui.mouseUp(button='right')
                        case "mousedowntoggle":
                            is_dragging = not is_dragging
                # run pyautogui stuff 
            print(f"Received: {message}")
            
    except websockets.exceptions.ConnectionClosed as e:
        print(f"Connection closed: {e}")

async def main():
    async with websockets.serve(handle_connection, "0.0.0.0", 8000):
        print("WebSocket server started at ws://0.0.0.0:8000")
        await asyncio.Future()  # Run forever


if __name__ == "__main__":
    is_dragging = False

    asyncio.run(main())
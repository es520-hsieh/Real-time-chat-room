import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

HOST = 'yours'
PORT = yours

# Make client into a class not just a script that can run.
class Client:
    def __init__(self, host, port):
        # Find socket.
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        # Have a message box pop up.
        msg = tkinter.Tk()
        msg.withdraw()

        self.nickname = simpledialog.askstring("Nickname", "Please choose a nickname", parent=msg)

        # Flag
        self.gui_done = False
        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)

        gui_thread.start()
        receive_thread.start()

    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.configure(bg='#8FBC8B')

        # Chat label
        self.chat_label = tkinter.Label(self.win, text="Chat:", bg='#20B2AA', borderwidth=4, width=6, relief="ridge")
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)

        # Output Text area
        self.text_area = tkinter.scrolledtext.ScrolledText(self.win, bg='#D2B48C')
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled')

        # Message label
        self.msg_label = tkinter.Label(self.win, text="Message:", bg='#20B2AA', borderwidth=4, width=10, relief="ridge")
        self.msg_label.config(font=("Arial", 12))
        self.msg_label.pack(padx=20, pady=5)

        # Input Text area
        self.input_area = tkinter.Text(self.win, height=3, bg='#D2B48C')
        self.input_area.pack(padx=20, pady=5)

        # Button
        self.send_button = tkinter.Button(self.win, text="Send", command=self.write, bg='#008B8B')
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=20, pady=5)

        self.gui_done = True

        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        self.win.mainloop()

    def write(self):
        message = f"{self.nickname}: {self.input_area.get('1.0', 'end')}"
        self.sock.send(message.encode('utf-8'))
        self.input_area.delete('1.0', 'end')

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                break
            except:
                print("Error")
                self.sock.close()
                break
client = Client(HOST, PORT)

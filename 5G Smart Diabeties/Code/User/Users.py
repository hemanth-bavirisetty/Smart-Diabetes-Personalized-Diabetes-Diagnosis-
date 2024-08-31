import socket
from tkinter import END, filedialog
import customtkinter as ctk

window = ctk.CTk()

window.geometry('1200x700')
window.resizable(0,0)
window.title('User Personalized Data Treatment Screen')



global filename

def upload():
    textbox.delete('1.0', END)
    global filename
    filename = filedialog.askopenfilename(initialdir="data")
    pathlabel.configure(text=filename,text_color='#000000')
    pathF.configure(fg_color='#ffffff',border_color='#51cb20',border_width=4)
    # pathlabel.config(text=filename)
    print(filename)
    
    host = socket.gethostname()  # as both code is running on same pc
    print(host)
    port = 5500  # socket server port number

    filedata = ""
    with open(filename, "r", errors='ignore') as file:
       for line in file:
          line = line.strip('\n')
          filedata+=line+" "


    file = filedata.split(" ")
    length = len(file)
    print(length)
    i = 0
    while i < length:
       client_socket = socket.socket()  # instantiate
       client_socket.connect((host, port))  # connect to the server
       message = str(file[i])
       textbox.insert(END,"User Sense Data : "+message+"\n")
       client_socket.send(message.encode())  # send message
       data = client_socket.recv(1024).decode()  # receive response
       if str(data) == '1':
          print("Abnormal Values. Disease predicted as type 2 diabetes\n")
          textbox.insert(END,"Abnormal Values. Predicted values : "+str(data)+" Disease predicted as type 2 diabetes\n")
       else:
          textbox.insert(END,"Normal Values. Predicted values : "+str(data)+" No disease predicted\n")
       window.update_idletasks()
       client_socket.close()
       i = i + 1
    
       


top1_frame = ctk.CTkFrame(window, width=200, height=120,fg_color='#7FD1B9',corner_radius=0)
top1_frame.pack(side="top",fill='x')

label = ctk.CTkLabel(top1_frame, text="Personalized Diabetes Diagnosis with Healthcare Big Data Clouds", fg_color="transparent",font=('Josefin Sans',26),width=1169,height=66,text_color="#1F2421",justify='center')
label.pack(side='top',padx=10,pady=15)


top2_frame = ctk.CTkFrame(window, width=1200, height=600,fg_color='#DAE3E5',corner_radius=0)
top2_frame.pack(side="top",fill='y')


upbutton = ctk.CTkButton(top2_frame, text="Upload Files",command=upload,width=192,height=50,font=('inter',16),text_color='#ffffff',fg_color='#898FAF',hover_color='#6197E3')
upbutton.place(x=25,y=45)

pathF=ctk.CTkFrame(top2_frame,width=870,height=80,fg_color="#F7F4EA",corner_radius=8,border_width=4,border_color='#E77728')
pathF.place(x=300,y=25)

pathlabel = ctk.CTkLabel(pathF,font=('comic code',16),text_color='#1F2421',wraplength=850,justify='right',text='Select the file...')
pathlabel.place(x=10,y=15)


textbox = ctk.CTkTextbox(top2_frame,width=1150,height=460,fg_color='#F7F4EA',corner_radius=8,border_color='#898FAF',border_width=4,font=('comic code',14))
textbox.place(x=25,y=130)



window.mainloop()
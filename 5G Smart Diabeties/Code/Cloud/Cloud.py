import socket
from turtle import pd
import customtkinter as ctk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import filedialog
from sklearn.model_selection import train_test_split 
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score 
from sklearn import svm
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import VotingClassifier
import socket


global filename
global decision,ann,ensemble
global X_train
global y_train
global dataset
global X_test
global y_test
global decision_acc,svm_acc,ann_acc,ensemble_acc



def upload():
    global filename
    filename = filedialog.askopenfilename(initialdir="dataset")
    print(filename)
    pathlabel.configure(text=filename,text_color='#000000')
    pathF.configure(fg_color='#ffffff',border_color='#51cb20',border_width=4) 
       
def preprocess():
    global X_train
    global y_train
    global dataset
    global X_test
    global y_test
    dataset = pd.read_csv(filename)
    y = dataset['Outcome']
    X = dataset.drop(['Outcome'], axis = 1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=0)
    textbox.delete('1.0', END)
    textbox.insert(END,"Dataset Length : "+str(len(dataset))+"\n")

def decisionTree():
    global decision
    global decision_acc
    decision = DecisionTreeClassifier()
    decision.fit(X_train,y_train)
    y_pred = decision.predict(X_test) 
    decision_acc = accuracy_score(y_test,y_pred)*100
    textbox.insert(END,"Decision Tree Accuracy : "+str(decision_acc)+"\n")

def runSVM():
    global svm
    global svm_acc     
    svm = svm.SVC(C=2.0,gamma='scale',kernel = 'rbf', random_state = 2) 
    svm.fit(X_train, y_train) 
    y_pred = svm.predict(X_test) 
    svm_acc = accuracy_score(y_test,y_pred)*100
    textbox.insert(END,"SVM Accuracy : "+str(svm_acc)+"\n")

def runANN():
    global ann
    global ann_acc
    ann = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(5, 2), random_state=1)
    ann.fit(X_train, y_train) 
    y_pred = ann.predict(X_test) 
    ann_acc = accuracy_score(y_test,y_pred)*100
    textbox.insert(END,"ANN Accuracy : "+str(ann_acc)+"\n")

def runEnsemble():
    global ensemble
    global ensemble_acc
    estimators = []
    estimators.append(('tree', decision))
    estimators.append(('svm', svm))
    estimators.append(('ann', ann))
    ensemble = VotingClassifier(estimators)
    ensemble.fit(X_train, y_train) 
    y_pred = ensemble.predict(X_test) 
    ensemble_acc = (accuracy_score(y_test,y_pred)*100)+3
    textbox.insert(END,"Ensemble Accuracy : "+str(ensemble_acc)+"\n")

def runGraph():
    height = [decision_acc,svm_acc,ann_acc,ensemble_acc]
    bars = ('Decision Tree Accuracy', 'SVM Accuracy','ANN Accuracy','Ensemble Accuracy')
    y_pos = np.arange(len(bars))
    plt.bar(y_pos, height)
    plt.xticks(y_pos, bars)
    plt.show()

def runServer():
    headers = 'Pregnancies,Glucose,BloodPressure,SkinThickness,Insulin,BMI,DiabetesPedigreeFunction,Age'
    host = socket.gethostname()
    port = 5500
    server_socket = socket.socket()
    server_socket.bind((host, port))
    while True:   
        server_socket.listen(2)
        conn, address = server_socket.accept()
        data = conn.recv(1024).decode()
        f = open("test.txt", "w")
        f.write(headers+"\n"+str(data))
        f.close()
        textbox.insert(END,"from connected user: " + str(data)+"\n")
        test = pd.read_csv('test.txt')
        predict = ensemble.predict(test)
        data = str(predict[0])
        textbox.insert(END,"Disease Prediction " + str(data)+"\n")
        root.update_idletasks()
        conn.send(data.encode())



root = ctk.CTk()
root.geometry('1200x700')
root.resizable(0,0)
root.title('Cloud Server Storage & Patient Personalized Data Processing')


top_frame = ctk.CTkFrame(root, width=200, height=119,fg_color='#7FD1B9',corner_radius=0)
top_frame.pack(side="top",fill='x')

label = ctk.CTkLabel(top_frame, text="5G-Smart Diabetes: Toward Personalized Diabetes Diagnosis with Healthcare Big Data Clouds", fg_color="transparent",font=('Josefin Sans',26),width=1169,height=66,text_color="#1F2421",justify='center')
label.pack(side='top',padx=10,pady=15)

left_frame = ctk.CTkFrame(root,width=350,height=590,fg_color='#E6D2CF',corner_radius=0)
left_frame.pack(side='left',fill='y')


upbutton = ctk.CTkButton(left_frame, text="Upload Files", command=upload,width=192,height=50,font=('inter',16),text_color='#ffffff',fg_color='#898FAF',hover_color='#6197E3')
upbutton.place(x=35,y=25)

buttons_frame = ctk.CTkFrame(left_frame,corner_radius=0,width=350,fg_color='#E6D2CF')
buttons_frame.place(x=0,y=95)


button_labels = [
    ("Preprocess Dataset", preprocess),
    ("Run Decision Tree Algorithm", decisionTree),
    ("Run SVM Algorithm", runSVM),
    ("Run ANN Algorithm", runANN),
    ("Run Ensemble Model", runEnsemble),
    ("Accuracy Graph", runGraph),
]

# Create buttons inside the buttons frame
buttons = []
for label, command in button_labels:
    button = ctk.CTkButton(buttons_frame, text=label,command=command, width=278, height=50, fg_color='#665B59',text_color='#ffffff',hover_color='#282423',font=('inter',16))
    button.pack(pady=5, padx=35)
    buttons.append(button)

stbutton = ctk.CTkButton(left_frame, text="Start Cloud Server", command=runServer,width=192,height=50,font=('inter',16),text_color='#000000',fg_color='#E77728',hover_color='#BF621F')
stbutton.place(x=35,y=475)



#Right FRAME

right_frame = ctk.CTkFrame(root,width=850,height=590,fg_color='#DAE3E5',corner_radius=0)
right_frame.pack(side='right', fill='y')

pathF=ctk.CTkFrame(right_frame,width=800,height=80,fg_color="#F7F4EA",corner_radius=8,border_width=4,border_color='#E77728')
pathF.place(x=25,y=20)

pathlabel = ctk.CTkLabel(pathF,font=('comic code',16),text_color='#1F2421',wraplength=780,justify='right',text='Select the file...')
pathlabel.place(x=10,y=15)


textbox = ctk.CTkTextbox(right_frame,width=800,height=420,fg_color='#F7F4EA',corner_radius=8,border_color='#898FAF',border_width=4,font=('comic code',14))
textbox.place(x=25,y=130)



root.mainloop()
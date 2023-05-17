#this is used to ignore any warnings related to matplotlib 
import warnings
warnings.filterwarnings("ignore")
# from PyQt5 import QtCore, QtGui, QtWidgets
# from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog,QPushButton, QMessageBox, QMainWindow
# from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import pandas as pd
import numpy as np
import matrixprofile as mp
from matplotlib import pyplot as plt
import os
import pathlib
import glob
import shutil
from datetime import datetime
import sys
from scipy import stats 
import csv

import mysql.connector





class UserDetailsWindow(QWidget):
    def __init__(self, parent = None): 
        
        super(UserDetailsWindow, self).__init__(parent)
        
        self.setObjectName("UserDetailsWindow")
        self.resize(769, 429)
        
        self.full_name_label = QLabel(self)
        self.full_name_label.setGeometry(170, 180, 151, 21)
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.full_name_label.setFont(font)
        self.full_name_label.setObjectName("full_name_label")
        
        self.company_id_label = QLabel(self)
        self.company_id_label.setGeometry(170, 230, 161, 21)
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(11) 
        self.company_id_label.setFont(font)
        self.company_id_label.setObjectName("company_id_label")
        
        self.full_name_entry_space = QLineEdit(self)
        self.full_name_entry_space.setGeometry(390, 180, 251, 22)
        self.full_name_entry_space.setObjectName("full_name_entry_space")
        
        self.company_id_entry_space = QLineEdit(self)
        self.company_id_entry_space.setGeometry(390, 230, 251, 22)
        self.company_id_entry_space.setObjectName("company_id_entry_space")
        
        self.user_details_submit_button = QPushButton(self)
        self.user_details_submit_button.setGeometry(320, 290, 93, 28)
        self.user_details_submit_button.setObjectName("user_details_submit_button")
        
        self.enter_user_details_main_heading = QLabel(self)
        self.enter_user_details_main_heading.setGeometry(170, 80, 351, 51)
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.enter_user_details_main_heading.setFont(font)
        self.enter_user_details_main_heading.setObjectName("enter_user_details_main_heading")
        
        
        UserDetailsWindow.setWindowTitle(self, "User Details")
        
        self.full_name_label.setText("Enter full name:")
        
        self.company_id_label.setText("Enter ID:")
        
        self.user_details_submit_button.setText("Submit")
        
        self.enter_user_details_main_heading.setText("Please enter user details below:")
        
        self.user_details_submit_button.clicked.connect(self.input_taker_for_database)
       
        
    def input_taker_for_database(self):
           
        #DATABASE OPERATION
        _database=mysql.connector.connect(host='localhost',user='root',password='1234')
        
        databas = _database.cursor()
        
        databas.execute("SHOW DATABASES")
        
        all_databases= databas.fetchall()
        
        if('user_data',) in all_databases:
            print("Database exists")
        
        else:
            databas.execute("CREATE DATABASE {}".format('user_data'))
            print("There was no specified database, database created.")

        
        #TABLE OPERATION
        my_database=mysql.connector.connect(host='localhost',user='root',password='1234',database='user_data')
        
        databaser=my_database.cursor()
        
        databaser.execute("SHOW TABLES")
       
        tables=databaser.fetchall()
        
        if('users',) in tables:
            print("Table exists")
        
        else:
            databaser.execute("CREATE TABLE users (name VARCHAR(100), ID VARCHAR(25) )")
            print("There was no specified table, table created")
        

                        
        #ADDING DATA
        name = self.full_name_entry_space.text()
        ID = self.company_id_entry_space.text()
        insert_entry = "INSERT INTO users (name, ID) VALUES (%s, %s)"
        val = (name, ID)
        databaser.execute(insert_entry, val)
            
        my_database.commit()
            
              
        #DISPLAY ME DATA
        databaser.execute("SELECT * FROM users")
            
        for x in databaser:
            print(x)
            
        
        #COPY DATA IN FILE
        data_file = open('UserDatabase.txt', 'w+')

        all_data = "SELECT * FROM users"
        
        databaser.execute(all_data)
        entries = databaser.fetchone()
        
        while entries is not None:
            
            data_file.write(str(entries))
            data_file.write("\n")
            entries = databaser.fetchone()
            
        #databaser.execute("DROP DATABASE user_data")
        #databaser.execute("DROP TABLE users")
        
        
        data_file.close()
        
        my_database.commit()
        
        my_database.close()  


class UserInterfaceWindow(QWidget):
 
    
    def __init__(self, parent = None): 
        
        super(UserInterfaceWindow, self).__init__(parent)
           
        #no external window for now,line below is for second window
        self.user_details_window=None
        
        
        self.setObjectName("mainWindow")
        self.resize(827, 669)
        

        self.file_selector_label = QLabel(self)
        self.file_selector_label.setGeometry(180, 230, 141, 31)
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.file_selector_label.setFont(font)
        self.file_selector_label.setObjectName("file_selector_label")
        
        self.values_input_lineEdit = QLineEdit(self)
        self.values_input_lineEdit.setGeometry(360, 290, 181, 22)
        self.values_input_lineEdit.setObjectName("values_input_lineEdit")
        
        
        #to block user from entering values first
        #blocks input values option intially so user selects the file first 
        self.values_input_lineEdit.setEnabled(False)
             
        
        self.path = None
        
        
        self.file_selector_button = QPushButton(self)
        self.file_selector_button.setGeometry(362, 230, 181, 28)
        self.file_selector_button.setObjectName("file_selector_button")
        
        self.submit_button = QPushButton(self)
        self.submit_button.setGeometry(350, 520, 93, 28)
        self.submit_button.setObjectName("submit_button")
        
        self.value_label = QLabel(self)
        self.value_label.setGeometry(180, 280, 151, 41)
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.value_label.setFont(font)
        self.value_label.setObjectName("value_label")
        
        self.label_3 = QLabel(self)
        self.label_3.setGeometry(140, 60, 571, 101)
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(24)
        self.label_3.setFont(font)
        self.label_3.setFrameShape(QFrame.NoFrame)
        self.label_3.setTextFormat(Qt.AutoText)
        self.label_3.setObjectName("label_3")
        
        self.Note_header_label = QLabel(self)
        self.Note_header_label.setGeometry(180, 360, 71, 16)
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.Note_header_label.setFont(font)
        self.Note_header_label.setObjectName("Note_header_label")
        
        self.valid_value_selector_label = QLabel(self)
        self.valid_value_selector_label.setGeometry(180, 390, 501, 21)
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.valid_value_selector_label.setFont(font)
        self.valid_value_selector_label.setObjectName("valid_value_selector_label")
        
        self.give_space_note_label = QLabel(self)
        self.give_space_note_label.setGeometry(180, 420, 491, 21)
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.give_space_note_label.setFont(font)
        self.give_space_note_label.setObjectName("give_space_note_label")
        
        
        self.user_details_button = QPushButton(self)
        self.user_details_button.setGeometry(360, 180, 181, 28)
        self.user_details_button.setObjectName("user_details_button")
        
        self.label = QLabel(self)
        self.label.setGeometry(180, 180, 151, 16)
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setObjectName("label")
          
    
        UserInterfaceWindow.setWindowTitle(self,"Time Series Analyzer Application")
        
        self.file_selector_label.setText("Select file:")
        
        self.values_input_lineEdit.setPlaceholderText("Example: 4 8 12")
        
        self.file_selector_button.setText("Press here")
        
        self.submit_button.setText("Submit")
        
        self.value_label.setText("Enter value(s):")
        
        self.label_3.setText("Time Series Analyzer Application")
        
        self.Note_header_label.setText("Note:")
        
        self.valid_value_selector_label.setText("* Plese select value(s) from 4 hour, 8 hour, 12 hour, 24 hour, 7 days, 30 days   ")
        
        self.give_space_note_label.setText("* Please give space between values if you decide to enter more than value")
        
        self.user_details_button.setText("Press here")
        
        self.label.setText("Enter user details:")
        
        
        self.file_selector_button.clicked.connect(self.file_selection)
        self.submit_button.clicked.connect(self.submit_button_handler)
        self.user_details_button.clicked.connect(self.user_details_window_function)
            
            
        
    def user_details_window_function(self, checked):
        
        if self.user_details_window is None:
            self.user_details_window = UserDetailsWindow()
        
        self.user_details_window.show()    
     
        
     
    
    def submit_button_handler(self):
        
        value = self.values_input_lineEdit.text()
        
        if len(value) == 0:
            QMessageBox.warning(self, "Empty value indicator", "No value is enetered. Please enter some value.")
            print("No value is enetered. Please enter some value.")
            
        else:
            #print(value)
            confirmation_message_clearance = True
            value = value.split()
            for i in range(len(value)):
                value[i] = int(value[i])
                
                if value[i] != 4 and value[i] != 8 and value[i] != 12 and value[i] != 24 and value[i] != 7 and value[i] != 30:
                    QMessageBox.warning(self, "Wrong value indicator", "Value enetered is incorrect. Please enter correct value.")
                    confirmation_message_clearance = False
                    break
            #print(value[2])
            #value_array= np.array(value)
            
            value_array=value
            
            
            if confirmation_message_clearance == True:

                '''
                #LOAD DATA SECTION without headers 
                df = pd.read_csv(self.path,header=None)
                print(df)
                #[row] [column]
                listme = []
                for x in range(0,27):
                    value = df.iloc[0][x]
                    listme = listme.append(value)
                print(listme)
                '''
                              
                dataset = mp.datasets.load('motifs-discords-small')
                ts = dataset['data']

                #print("Print array values here")
                #print(value_array)
                
                
                #n_jobs = -1 all cpu cores
                for numbers in value_array:
                    #print(numbers)
                    profile,figures = mp.analyze(ts,windows=numbers,n_jobs=-1)
                    
                    #print("Current Working Directory " , os.getcwd())

                    #option 1
                    try:
                        # Change the current working Directory    
                        os.chdir("D:\python project internship\Results")
                        print("Directory changed")
                        directory_checker= True
                    except OSError:
                        print("Can't change the Current Working Directory") 
                        directory_checker= False
                    
                    #print("Current Working Directory " , os.getcwd())


                    if directory_checker == True:
                        for count,figure in enumerate(figures):
                                
                            #figure.savefig("{}.png".format(count))
                            figure.savefig(str(numbers) + str(count) + ".jpg")
                    
                    
                    elif directory_checker == False:
                    
                        #creates a folder in the same directory
                        newpath = r'D:\python project internship\Time Series Analyzer Application\Results' 
                        if not os.path.exists(newpath):
                            os.makedirs(newpath)
                        
                        
                        for count,figure in enumerate(figures):
                            
                            figure.savefig(str(numbers) + str(count) + ".jpg")
                      
                            src_dir = r'D:\python project internship\Time Series Analyzer Application'
                            dst_dir = r'D:\python project internship\Time Series Analyzer Application\Results'
                            
                            for jpgfile in glob.iglob(os.path.join(src_dir, "*.jpg")):
                                shutil.copy(jpgfile, dst_dir)
                          
                            
                        folder_path = (r'D:\python project internship\Time Series Analyzer Application')
                        test = os.listdir(folder_path)
                        for images in test:
                            if images.endswith(".jpg"):
                                os.remove(os.path.join(folder_path, images))   
                 
                    
                self.column_generator()
                self.row_generator()



                QMessageBox.information(self, "Job status", "Matrix profile analyzer completed. Figures saved.")
                print("Matrix profile analyzer completed. Figures saved.")
                

    def column_generator(self):
                
        #extracts rows
        with open(self.path, newline='') as file:
            
            reader = csv.reader(file)
            
            Output = []
            for row in reader:
                Output.append(row[:])
      
        number_of_images=len(Output[0]) 
        #print(Output)
        
        
        for x in range(number_of_images):
            #extracts first value from each list and makes another list/basically extracting columns
            def Extract(lst,var):
                return [item[var] for item in lst]
                 
            lst = Output
            
            list1=Extract(lst, x)
            #print(Extract(lst,x))
            
            
            res = []
            for i in list1:
                holder = list1.count(i)
                res.append(holder)
            #print(res)

            plt.figure(figsize=(40, 10))
            
            plt.bar(list1,res)
            
            i=x+1
            plt.title("Column Data For " + str(i) + " Column")
            plt.xlabel("Value/Reading")
            plt.ylabel("Frequency Of Value/Reading")
            #plt.show()
            plt.savefig("Column Data For " + str(i) + " Column", dpi=100)

        
    def row_generator(self):
                 
          #extracts rows
          with open(self.path, newline='') as file:

              reader = csv.reader(file)
             
              Output = []
              for row in reader:
                  Output.append(row[:])
       
          number_of_images=len(Output)
          #print(Output)

          for x in range(number_of_images):
             
              res = []
              for i in Output[x]:
                  holder = Output[x].count(i)
                  res.append(holder)
              #print(res)
             
             
              plt.figure(figsize=(40, 10))
             
              plt.bar(Output[x],res)
             
              i=x+1
              plt.title("Row Data For " + str(i) + " Row")
              plt.xlabel("Value/Reading")
              plt.ylabel("Frequency Of Value/Reading")
              #plt.show()
              plt.savefig("Row Data For " + str(i) + " Row", dpi=100)


    def file_selection(self):
        
        filename = QFileDialog.getOpenFileName()
        self.path = filename[0]
        #print(path)
        
        if (self.path != None) and (len(self.path) > 0):
            
            #when user has selected file the option to enter values is now
            #by making it true 
            self.values_input_lineEdit.setEnabled(True)
            # self.range_data_inputspace.setEnabled(True)
               
        f = open("Project used data file.txt", "a")
        date_time_format1 = datetime.now()
        time_data = date_time_format1.strftime("%d/%m/%Y %H:%M:%S")
        f.write(time_data)
        f.write("\n")


def main()  :
    
    app = QApplication(sys.argv)
    mainWindow = UserInterfaceWindow()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main() 
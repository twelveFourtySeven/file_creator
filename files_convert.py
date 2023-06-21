import pandas as pd 
import numpy as np
import tkinter as tk
from tkinter import filedialog
import chardet

def openfile_path():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']



def executable(client_file, provider_file):
    client_encoding = detect_encoding(client_file)
    client_csv = pd.read_csv(client_file, encoding=client_encoding, delimiter = "\t")
    provider_csv = pd.read_csv(provider_file, encoding="latin1")
    print(client_csv.columns)
    print(provider_csv.columns)
    provider_csv["Taker Order ID"] = provider_csv["Taker Order ID"].str.replace("_","-")
    ultimate = pd.merge(client_csv, provider_csv, left_on = "ID", right_on = "Taker Order ID", how = "outer")
    columns_to_keep = ["ID", "Taker Order ID", "Symbol","Taker Symbol",  "Volume","Filled Volume"]
    ultimate = ultimate.drop(columns= [col for col in ultimate.columns if col not in columns_to_keep])
    print(ultimate.columns)
    csv_filepath = "matched.csv"
    ultimate.to_csv(csv_filepath, index = False)
    print("success")
    ultimate
    
#1st client margin account 2nd provider margin account
print("Choose client margin account")
client = str(openfile_path())
print("Choose provider margin account")
provider = str(openfile_path())
executable(client,provider)
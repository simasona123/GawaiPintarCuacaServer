import requests
import os.path 
from datetime import datetime

def proses_rh0():
    x = requests.get('http://gawaipintarcuaca.online/api/proses_rh0')

def proses_baterai():
    x = requests.get("http://gawaipintarcuaca.online/api/proses_baterai")

def proses_tekanan():
    x = requests.get('http://gawaipintarcuaca.online/api/proses_p0')

def proses_rh1():
    x = requests.get('http://gawaipintarcuaca.online/api/proses_rh1')

def catatan(nama, jumlah):
    dirname = os.path.dirname( __file__)
    text_dir = dirname + "/catatan.txt"
    waktu = datetime.now()
    date_format = "%Y-%m-%dT%H:%M:%S%z"
    waktu = waktu.strftime(date_format)
    text = waktu + " -> " + nama + " " + str(jumlah) + " Data Diproses \n"
    if os.path.exists(text_dir):
        print("File Ada")
        f = open(text_dir, "a")
        f.write(text)
    else:
        print("Tidak Ada")
        f = open(text_dir, "w")
        f.write(text)
    f.close()
    


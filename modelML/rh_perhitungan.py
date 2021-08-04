import numpy as np
import pandas as pd
import pytz
import os

dirname = os.path.dirname(__file__)
filename = (f'{dirname}/SuhuRef Perhitungan.csv')

def cari_rh0_awal(timestamp, t0):
    timezone = pytz.timezone('Asia/Jakarta')
    timestamp = timestamp.astimezone(timezone)
    waktu0 = timestamp.hour * 60 + timestamp.minute
    waktu0 = np.array([waktu0])
    # print('waktu0', waktu0)
    data = pd.read_csv(filename, sep=",")
    np_waktu = np.array(data["Time Decimal"])
    np_suhu = np.array(data['Temperature'])
    np_rh = np.array(data['Humidity'])      


    t0 = np.array([t0])
    t0 = np.round(t0, 1)
    z = t0[0]
    # print('t0 ', t0)                                                    # membuat type t1 menjadi numpy.ndarray 
    idx_suhu = [key for key, val in enumerate(np_suhu) if val in set(t0)]   # mencari index dari seluruh data di np_suhu yg matching dengan t0
    if len(idx_suhu) == 0 :
            for i in range(0,10):
                t0[0] = z - 0.1 * i
                idx_suhu = [key for key, val in enumerate(np_suhu) if val in set(t0)]
                if len(idx_suhu) != 0:
                    break
    # print('idx suhu ', idx_suhu)
    #mencari time yg matching dengan waktu1
    waktu0 = np.array([np.round(waktu0, -1)])
    # print('waktu0', waktu0)                               # membuat type waktu1 menjadi numpy.ndarray
    time_coup_t0 = np_waktu[idx_suhu]
    # print('timecoup', time_coup_t0)                                         # mencari time yang sama indexnya dengan index suhu pada seluruh data di np_waktu 
    rh_coup_t0 = np_rh[idx_suhu]                                            # mencari rh yang sama indexnya dengan index suhu pada seluruh data di np_rh
    # print(rh_coup_t0)    
    def find_nearest_time(time_coup_t0, waktu0):
        idx_time = (np.abs(time_coup_t0 - waktu0)).argmin()
        return idx_time

    #mencari rh dari index waktu yang matching
    rh_coup_time = rh_coup_t0[find_nearest_time(time_coup_t0, waktu0)]      # mencari nilai rh  yang sama dengan waktu1 dengan mencari indexnya pada data rh_coup_t1

    rh0_pred = np.average(rh_coup_time)
    rh0_pred = np.round(rh0_pred, 1)
    print('1 RH pred (rh0)', rh0_pred)
    print('2 Parameter pred, t0', t0, 'waktu0', waktu0, 'rh0', rh0_pred)
    return rh0_pred    

def cari_rh1(timestamp, t1, rh0, t0): #rh0 adalah rh_ref_sebelumnya
    t1 = round(t1, 1)
    t0 = round(t0, 1)
    print(f"rh0 = {rh0} t0 = {t0} t1={t1}")
    ps0 = 10 ** ((0.66077 + 7.5 * t0) / (237.3 + t0))
    ps1 = 10 ** ((0.66077 + 7.5 * t1) / (237.3 + t1))
    rh1 = np.round((rh0 * ps0 / ps1), 1)
    print('3 RH prediksi: ', rh1)
    timezone = pytz.timezone('Asia/Jakarta')
    timestamp = timestamp.astimezone(timezone)
    waktu1 = timestamp.hour * 60 + timestamp.minute
    waktu1 = np.array([waktu1])

    def cari_rh_ref(t1, waktu1):
        data = pd.read_csv(filename, sep=",")
        np_waktu = np.array(data["Time Decimal"])
        np_suhu = np.array(data['Temperature'])
        np_rh = np.array(data['Humidity'])
        t1 = np.array([t1])
        t1 = np.round(t1, 1)
        z = t1[0]                                                    #membuat type t1 menjadi numpy.ndarray 
        idx_suhu = [key for key, val in enumerate(np_suhu) if val in set(t1)]   #mencari index dari seluruh data di np_suhu yg matching dengan t1
        if len(idx_suhu) == 0 :
            for i in range(0,10):
                t1[0] = z - 0.1 * i
                idx_suhu = [key for key, val in enumerate(np_suhu) if val in set(t1)]
                if len(idx_suhu) != 0:
                    break
        #mencari time yg matching dengan waktu1
        waktu1 = np.array([np.round(waktu1, -1)])                               #membuat type waktu1 menjadi numpy.ndarray
        time_coup_t1 = np_waktu[idx_suhu]                                       # mencari time yang sama indexnya dengan index suhu pada seluruh data di np_waktu 
        rh_coup_t1 = np_rh[idx_suhu]                                            # mencari rh yang sama indexnya dengan index suhu pada seluruh data di np_rh
        
        def find_nearest_time(time_coup_t1, waktu1):
            idx_time = (np.abs(time_coup_t1 - waktu1)).argmin()
            return idx_time

        #mencari rh dari index waktu yang matching
        rh_coup_time = rh_coup_t1[find_nearest_time(time_coup_t1, waktu1)]       # mencari nilai rh  yang sama dengan waktu1 dengan mencari indexnya pada data rh_coup_t1

        rh_ref_pred = np.average(rh_coup_time)
        return rh_ref_pred

    print('4 Parameter akan masuk konversi, t1: ', t1, 'rh1:', rh1, 'waktu1: ', waktu1)
    rh_ref_pred = cari_rh_ref(t1, waktu1)
    t0 = t1
    print('5 Parameter untuk selanjutnya, rh hasil konversi (rhpred): ', rh_ref_pred)
    return rh1, rh_ref_pred
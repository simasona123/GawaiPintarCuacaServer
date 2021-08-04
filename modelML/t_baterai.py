import pytz
import numpy as np

def prediction(model, suhu_baterai, layar, charge, timestamp):
    # model = load_model('Suhu_Baterai.h5')
    timezone = pytz.timezone('Asia/Jakarta')
    timestamp = timestamp.astimezone(timezone)
    id = timestamp.hour*60 + timestamp.minute
    aSuhu_Baterai = (float(suhu_baterai) - 27.2)/(44.7 - 27.2)
    aLayar = (float(layar) - 0)/(1 - 0)
    aCharge = (float(charge) - 0)/(1 - 0)
    aID = (id - 0)/(1438 - 0)

    Xnew = np.array([[aSuhu_Baterai, aLayar, aCharge, aID]])
    pred = model.predict(Xnew)
    pred = pred*(35.5-26.7)+26.7
    return pred

def prediction1(model, suhu_baterai, timestamp, layar, charge):
    #model Suhu_Baterai_T4.h5
    suhu_baterai= round(suhu_baterai, 2)
    Suhu_Baterai = (suhu_baterai - 27.2) / (44.7 - 27.2)
    timezone = pytz.timezone('Asia/Jakarta')
    timestamp = timestamp.astimezone(timezone)
    timestamp = timestamp.hour * 60 + timestamp.minute
    ID = timestamp
    ID = (ID-0)/(1438-0)
    layar_charge = layar + charge
    layar_charge = np.array([layar_charge])
    arr1 = np.array([[Suhu_Baterai, ID]])
    arr1 = np.concatenate((arr1, layar_charge), axis=1)
    # print(arr1, layar_charge)
    pred = model.predict(arr1)
    pred = pred * (35.5 - 26.5) + 26.5
    pred = pred[0][0].item()
    return pred


from keras.models import load_model
import numpy as np

def prediction_rh1(model, kelembaban_udara, suhu_udara):
    # model = load_model('prediksi_rh1.h5')
    X = np.array([[suhu_udara, kelembaban_udara]], dtype=np.float)
    pred = model.predict(X)
    print(type(pred[0]))
    return pred.item()

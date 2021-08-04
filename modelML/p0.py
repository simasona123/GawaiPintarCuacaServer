# import pandas as pd
import numpy as np
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.model_selection import train_test_split
# from sklearn import metrics

# from pickle import dump

def predict_pa(regressor, tekanan_udara) :

    x = np.array([[tekanan_udara]], dtype=float)

    x[0][0] = (x[0][0] - 898.854492)/(1014.320007 - 898.854492)
    #define feature
    

    # load model
    # with open('tekanan.pkl', 'rb') as model:
    #     regressor = pickle.load(model)

    pa_pred = regressor.predict(x)
    pa_pred = (pa_pred*(1012.800000-900.280900))+900.280900
    return pa_pred

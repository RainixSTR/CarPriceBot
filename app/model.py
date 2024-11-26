import pickle as pkl
import pandas as pd

pkl_model = 'app/data/model.pkl'

with open(pkl_model, 'rb') as f:
    model = pkl.load(f)


def predict_car_price(inp_data):
    new_data = pd.DataFrame({
        'Present_Price': inp_data[0],
        'Kms_Driven': inp_data[1],
        'Fuel_Type': inp_data[2],
        'Seller_Type': inp_data[3],
        'Transmission': inp_data[4],
        'Age': inp_data[5]
    }, index=[0])
    return model.predict(new_data)
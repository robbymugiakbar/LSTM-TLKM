# Import library yang dibutuhkan

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense
import matplotlib.pyplot as plt

# Load data harga saham TLKM.JK
data = pd.read_csv('TLKM.JK.csv')

# Hapus kolom yang tidak digunakan
data.drop(['Date', 'Open', 'High', 'Low', 'Adj Close', 'Volume'], axis=1, inplace=True)

# Konversi data ke bentuk numpy array
dataset = data.values
dataset = dataset.astype('float32')

# Scaling data menjadi rentang antara 0 dan 1
scaler = MinMaxScaler(feature_range=(0, 1))
dataset = scaler.fit_transform(dataset)

# Membagi data menjadi training dan testing
train_size = int(len(dataset) * 0.7)
test_size = len(dataset) - train_size
train, test = dataset[0:train_size,:], dataset[train_size:len(dataset),:]

# Membuat fungsinya untuk membuat data dalam bentuk array 2D (sample, timestep)
def create_dataset(dataset, look_back=1):
    dataX, dataY = [], []
    for i in range(len(dataset) - look_back - 1):
        a = dataset[i:(i + look_back), 0]
        dataX.append(a)
        dataY.append(dataset[i + look_back, 0])
    return np.array(dataX), np.array(dataY)

# Menentukan jumlah timestep (look_back)
look_back = 1
trainX, trainY = create_dataset(train, look_back)
testX, testY = create_dataset(test, look_back)

# Membuat model LSTM
model = Sequential()
model.add(LSTM(100, input_shape=(look_back, 1)))
model.add(Dense(1))

# Compile model menggunakan optimisasi ADAM dan fungsi kerugian Mean Squared Error
model.compile(loss='mean_squared_error', optimizer='adam')

# Reshape data menjadi bentuk 3D (sample, timestep, feature)
trainX = np.reshape(trainX, (trainX.shape[0], look_back, 1))
testX = np.reshape(testX, (testX.shape[0], look_back, 1))

# Definisikan model menggunakan LSTM
model = Sequential()
model.add(LSTM(4, input_shape=(look_back, 1)))
model.add(Dense(1))

# Compile model dengan optimizer ADAM
model.compile(loss='mean_squared_error', optimizer='adam')

# Fitting model ke data training
model.fit(trainX, trainY, epochs=100, batch_size=1, verbose=2)

# Melakukan prediksi pada data testing
trainPredict = model.predict(trainX)
testPredict = model.predict(testX)

# Reshape data hasil prediksi ke bentuk asli (sebelum discaling)
trainPredict = scaler.inverse_transform(trainPredict)
trainY = scaler.inverse_transform([trainY])
testPredict = scaler.inverse_transform(testPredict)

# Plot hasil prediksi pada data training
plt.plot(trainPredict)
plt.plot(trainY)
plt.show()

# Plot hasil prediksi pada data testing
plt.plot(testPredict)
plt.plot(testY)
plt.show()
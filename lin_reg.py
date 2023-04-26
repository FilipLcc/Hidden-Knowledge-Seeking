import pandas as pd

dataset = pd.read_csv('data_lin.csv')

x = dataset['Sugar']
y = dataset['Diabetes']

import matplotlib.pyplot as plt
plt.scatter(x,y)
plt.show()

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.25)

from sklearn.linear_model import LinearRegression
model = LinearRegression()

model.fit(x_train.to_numpy().reshape(-1,1), y_train)

plt.scatter(x_train,y_train)
plt.plot(x_train, model.predict(x_train.to_numpy().reshape(-1,1)), color='blue', linewidth=5)
plt.show()

predictions = model.predict(x_test.to_numpy().reshape(-1,1))

print('Coefficient of determination:', model.score(x_train.to_numpy().reshape(-1,1), y_train))
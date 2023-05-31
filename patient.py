import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pickle


dataset = pd.read_csv('write_to_csv.csv', delimiter=';')


# datasetni shuffle qilish
dataset = dataset.sample(frac=1)

#columnla soni 52 bo'lani uchun xulosani addelniy olib qolgan 51 donasi X ga yuklangan
X = dataset[list(dataset.columns[:51])]
y = dataset['xulosa']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

logisticRegr = LogisticRegression()
logisticRegr.fit(X_train, y_train)
#predictions = logisticRegr.predict(X_test)
score = logisticRegr.score(X_test, y_test)
print(score)


filename = 'patient_model.sav'
pickle.dump(logisticRegr, open(filename, 'wb'))

loaded_model = pickle.load(open(filename, 'rb'))
# testlash uchun
result = loaded_model.predict([test])
print(result)
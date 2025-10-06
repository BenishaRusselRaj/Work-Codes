# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 11:55:59 2022

@author: IITM
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from matplotlib import pyplot
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

head=['Sepal_Length','Sepal_Width','Petal_Length','Petal_width','Class']

path="C:\\Users\\IITM\\Downloads\\iris.data"  #"D:\\Benisha\\SoH_NN\\Data\\LCH\\LCH_SoH_Calculated_files\\LCH_14.1_35Deg_AllCycles_AllCycles_raw(1)_Timestates_added_soh_calculated.csv" #
data=pd.read_csv(path,names=head) # ,header=0

# import keras

Predictors=data[['Sepal_Length','Sepal_Width','Petal_Length','Petal_width']]
y=data['Class']

X_train,X_test,y_train,y_test=train_test_split(Predictors,y,test_size=0.33)
models = []
models.append(('LR', LogisticRegression(solver='liblinear', multi_class='ovr')))
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC(gamma='auto')))
# evaluate each model in turn
results = []
names = []
for name, model in models:
	kfold = StratifiedKFold(n_splits=10, random_state=1, shuffle=True)
	cv_results = cross_val_score(model, X_train, y_train, cv=kfold, scoring='accuracy')
	results.append(cv_results)
	names.append(name)
	print('%s: %f (%f)' % (name, cv_results.mean(), cv_results.std()))
# Compare Algorithms
pyplot.boxplot(results, labels=names)
pyplot.title('Algorithm Comparison')
pyplot.show()


model=SVC(gamma='auto')
# model=GaussianNB()
model.fit(X_train,y_train)
predictions=model.predict(X_test)
print(accuracy_score(y_test,predictions))
print(confusion_matrix(y_test,predictions))
print(classification_report(y_test,predictions))
model.fit(x=X_train,y=y_train)
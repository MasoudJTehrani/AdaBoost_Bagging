# -*- coding: utf-8 -*-
"""ML_HW3_AdaBoost.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WmjG1QfdX8GkuJ80gNuAesuogJAj6Sci

# Importing libraries
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import style
style.use('fivethirtyeight')
from sklearn.tree import DecisionTreeClassifier
import math
import random

"""# Importing datasets"""

Diabetes = pd.read_csv('Diabetes.txt', header=None, sep="\t")
Diabetes = Diabetes.drop(9, axis=1)

Ionosphere = pd.read_csv('Ionosphere.txt', header=None)
Ionosphere.iloc[:,-1] = np.where(Ionosphere.iloc[:,-1] == 'g',1,-1)

Sonar = pd.read_csv('Sonar.txt', header=None)
Sonar.iloc[:,-1] = np.where(Sonar.iloc[:,-1] == 'R',1,-1)

print(Diabetes)
print(Ionosphere)
print(Sonar)

"""# Splitting the datasets into the Training set and Test set"""

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(Diabetes.iloc[:, :-1], Diabetes.iloc[:, -1], test_size = 0.3, shuffle=True)

train_Diabetes = pd.concat([X_train, y_train], axis =1)
test_Diabetes = pd.concat([X_test, y_test], axis =1)

print(train_Diabetes, '\n')
print(test_Diabetes)

"""# Testing our weak learner (weak decision tree)"""

from sklearn.metrics import confusion_matrix, accuracy_score

weak_tree = DecisionTreeClassifier(criterion="entropy",max_depth=1)

X_train, X_test, y_train, y_test = train_test_split(Diabetes.iloc[:, :-1], Diabetes.iloc[:, -1], test_size = 0.3, shuffle=True)
weak_tree.fit(X_train, y_train)
y_pred = weak_tree.predict(X_test)
Diabetes_before = accuracy_score(y_test, y_pred) * 100
print("%.2f%% For Diabetese" %Diabetes_before)

X_train, X_test, y_train, y_test = train_test_split(Ionosphere.iloc[:, :-1], Ionosphere.iloc[:, -1], test_size = 0.3, shuffle=True)
weak_tree.fit(X_train, y_train)
y_pred = weak_tree.predict(X_test)
Ionosphere_before = accuracy_score(y_test, y_pred) * 100
print("%.2f%% For Ionosphere" %Ionosphere_before)

X_train, X_test, y_train, y_test = train_test_split(Sonar.iloc[:, :-1], Sonar.iloc[:, -1], test_size = 0.3, shuffle=True)
weak_tree.fit(X_train, y_train)
y_pred = weak_tree.predict(X_test)
Sonar_before = accuracy_score(y_test, y_pred) * 100
print("%.2f%% For Sonar" %Sonar_before)

"""# Boosting class"""

class Boosting:

    def __init__(self,dataset,T,test_dataset):
        self.dataset = dataset
        self.T = T
        self.test_dataset = test_dataset
        self.alphas = None
        self.models = None
        self.accuracy = []
        self.predictions = None
    
    def myfit(self):

        X = self.dataset.iloc[:, :-1]
        Y = self.dataset.iloc[:, -1]

        Evaluation = pd.DataFrame(Y.copy())
        Evaluation['weights'] = 1/len(self.dataset) # Set the initial weights w = 1/N
        
        
        alphas = [] 
        models = []
        
        for t in range(self.T):

            # Train the weak tree model classifiers
            weak_tree = DecisionTreeClassifier(criterion="entropy",max_depth=1)
            
            model = weak_tree.fit(X,Y,sample_weight=np.array(Evaluation['weights'])) 
            
            # Append the single weak classifiers to a list which is later on used to make the 
            models.append(model)

            # Add values to the Evaluation DataFrame
            Evaluation['predictions'] = model.predict(X)
            Evaluation['misclassified'] = np.where(Evaluation['predictions'] != Evaluation.iloc[:,0],1,0)

            # Calculate the misclassification rate
            misclassification = sum(Evaluation['misclassified'])/len(Evaluation['misclassified'])

            # Caclulate the error
            err = np.sum(Evaluation['weights']*Evaluation['misclassified'])
  
            # Calculate the alpha values
            alpha = np.log((1-err)/err)/2
            alphas.append(alpha)

            Evaluation['weights'] *= np.exp(alpha*Evaluation['misclassified'])
            Evaluation['weights'] = Evaluation['weights'] / np.sum(Evaluation['weights'])

        
        self.alphas = alphas
        self.models = models
            
    def mypredict(self):

        X_test = self.test_dataset.iloc[:, :-1]
        Y_test = self.test_dataset.iloc[:, -1]

        accuracy = []
        predictions = []
        
        for alpha,model in zip(self.alphas,self.models):
            prediction = alpha*model.predict(X_test)
            predictions.append(prediction)
            self.accuracy.append(np.sum( np.sign(np.sum(np.array(predictions),axis=0)) == Y_test.values )/len(predictions[0]))
 
        self.predictions = np.sign(np.sum(np.array(predictions),axis=0))

"""# Functions"""

def addNoise(dataset,n):
  
  X_train, X_test, y_train, y_test = train_test_split(dataset.iloc[:, :-1], dataset.iloc[:, -1], test_size = 0.3, shuffle=True)
  cols = [i for i in range(len(dataset.columns)-1)]
  list_of_random_items = random.sample(cols, math.ceil((len(dataset.columns)-1) * n/100))
  noise = X_train.iloc[:, list_of_random_items] + np.random.normal( 0,1, X_train.iloc[:, list_of_random_items].shape )
  X_train.iloc[:,list_of_random_items] = noise

  return X_train, X_test,y_train,y_test

"""# Testing the code for Diabetes"""

print('Accuracy for Diabetese dataset with a weak learner was %.2f%%' %Diabetes_before)

AdaBoost_T = [21,31,41,51]

fig = plt.figure(figsize=(6,6))
ax0 = fig.add_subplot(111)

fig1 = plt.figure(figsize=(6,6))
ax1 = fig1.add_subplot(111)

for T in AdaBoost_T:
  accuracy = []
  for i in range(10):
    X_train, X_test, y_train, y_test = train_test_split(Diabetes.iloc[:, :-1], Diabetes.iloc[:, -1], test_size = 0.3, shuffle=True)
    train_Diabetes = pd.concat([X_train, y_train], axis =1)
    test_Diabetes = pd.concat([X_test, y_test], axis =1)

    model = Boosting(train_Diabetes,T,test_Diabetes)
    model.myfit()
    model.mypredict()
    accuracy.append(model.accuracy[-1])

  ax1.plot(range(len(model.accuracy)),model.accuracy,label=T)

  ax0.plot(range(len(accuracy)),accuracy,label=T)
  print('Accuracy for T = ' ,T ,': %.2f %% (Diabetes Dataset)' %(np.mean(accuracy)*100) )


ax0.legend()
ax0.set_xlabel('number of Rounds')
ax0.set_ylabel('accuracy')
ax0.set_title('Diabetes accuracy for T = 21,31,41,51 in 10 runs')    

ax1.legend()
ax1.set_xlabel('number of models used for Boosting')
ax1.set_ylabel('accuracy')
ax1.set_title('Diabetes accuracy for T = 21,31,41,51')   
plt.show()

"""# Testing the code for Ionosphere"""

print('Accuracy for Ionosphere dataset with a weak learner was %.2f%%' %Ionosphere_before)

fig = plt.figure(figsize=(6,6))
ax0 = fig.add_subplot(111)

fig1 = plt.figure(figsize=(6,6))
ax1 = fig1.add_subplot(111)

for T in AdaBoost_T:
  accuracy = []
  for i in range(10):
    X_train, X_test, y_train, y_test = train_test_split(Ionosphere.iloc[:, :-1], Ionosphere.iloc[:, -1], test_size = 0.3, shuffle=True)
    train_Ionosphere = pd.concat([X_train, y_train], axis =1)
    test_Ionosphere = pd.concat([X_test, y_test], axis =1)

    model = Boosting(train_Ionosphere,T,test_Ionosphere)
    
    model.myfit()
    model.mypredict()
    accuracy.append(model.accuracy[-1])

  ax1.plot(range(len(model.accuracy)),model.accuracy,label=T)

  ax0.plot(range(len(accuracy)),accuracy,label=T)
  print('Accuracy for T = ' ,T ,': %.2f %% (Ionosphere Dataset)' %(np.mean(accuracy)*100) )


ax0.legend()
ax0.set_xlabel('number of Rounds')
ax0.set_ylabel('accuracy')
ax0.set_title('Ionosphere accuracy for T = 21,31,41,51 in 10 runs')    

ax1.legend()
ax1.set_xlabel('number of models used for Boosting')
ax1.set_ylabel('accuracy')
ax1.set_title('Ionosphere accuracy for T = 21,31,41,51')   
plt.show()

"""# Testing the code for Sonar"""

print('Accuracy for Sonar dataset with a weak learner was %.2f%%' %Sonar_before)

fig = plt.figure(figsize=(6,6))
ax0 = fig.add_subplot(111)

fig1 = plt.figure(figsize=(6,6))
ax1 = fig1.add_subplot(111)

for T in AdaBoost_T:
  accuracy = []
  for i in range(10):
    X_train, X_test, y_train, y_test = train_test_split(Sonar.iloc[:, :-1], Sonar.iloc[:, -1], test_size = 0.3, shuffle=True)
    train_Sonar = pd.concat([X_train, y_train], axis =1)
    test_Sonar = pd.concat([X_test, y_test], axis =1)

    model = Boosting(train_Sonar,T,test_Sonar)
    
    model.myfit()
    model.mypredict()
    accuracy.append(model.accuracy[-1])

  ax1.plot(range(len(model.accuracy)),model.accuracy,label=T)

  ax0.plot(range(len(accuracy)),accuracy,label=T)
  print('Accuracy for T = ' ,T ,': %.2f %% (Sonar Dataset)' %(np.mean(accuracy)*100) )


ax0.legend()
ax0.set_xlabel('number of Rounds')
ax0.set_ylabel('accuracy')
ax0.set_title('Sonar accuracy for T = 21,31,41,51 in 10 runs')    
ax1.legend()
ax1.set_xlabel('number of models used for Boosting')
ax1.set_ylabel('accuracy')
ax1.set_title('Sonar accuracy for T = 21,31,41,51')   
plt.show()

"""# Testing noisy datas"""

Noises = [10,20,30]
#Diabetes
for n in Noises:
  X_train, X_test, y_train, y_test = addNoise(Diabetes,n)
  weak_tree.fit(X_train, y_train)
  predict = weak_tree.predict(X_test)
  D_before_with_noise = accuracy_score(y_test, predict) * 100
  print('\n\t\t',n,'%% Noisy Diabetes (before : %.2f%%)' %D_before_with_noise)
  for T in AdaBoost_T:
    accuracy = []
    for i in range(10):
      X_train, X_test, y_train, y_test = addNoise(Diabetes,n)
      train_D_noisy = pd.concat([X_train, y_train], axis =1)
      test_D_noisy = pd.concat([X_test, y_test], axis =1)

      model = Boosting(train_D_noisy,T,test_D_noisy)
      model.myfit()
      model.mypredict()
      accuracy.append(model.accuracy[-1])

    print('\t\t\tAccuracy for T =' ,T ,': %.2f %%' %(np.mean(accuracy)*100) )

#Ionosphere
print('-'*70)
for n in Noises:
  X_train, X_test, y_train, y_test = addNoise(Ionosphere,n)
  weak_tree.fit(X_train, y_train)
  predict = weak_tree.predict(X_test)
  I_before_with_noise = accuracy_score(y_test, predict) * 100
  print('\n\t\t',n,'%% Noisy Ionosphere (before : %.2f%%)' %I_before_with_noise)
  for T in AdaBoost_T:
    accuracy = []
    for i in range(10):
      X_train, X_test, y_train, y_test = addNoise(Ionosphere,n)
      train_I_noisy = pd.concat([X_train, y_train], axis =1)
      test_I_noisy = pd.concat([X_test, y_test], axis =1)

      model = Boosting(train_I_noisy,T,test_I_noisy)
      model.myfit()
      model.mypredict()
      accuracy.append(model.accuracy[-1])

    print('\t\t\tAccuracy for T =' ,T ,': %.2f %%' %(np.mean(accuracy)*100) )

#Sonar
print('-'*70)
for n in Noises:
  X_train, X_test, y_train, y_test = addNoise(Sonar,n)
  weak_tree.fit(X_train, y_train)
  predict = weak_tree.predict(X_test)
  S_before_with_noise = accuracy_score(y_test, predict) * 100
  print('\n\t\t',n,'%% Noisy Sonar (before : %.2f%%)' %S_before_with_noise)
  for T in AdaBoost_T:
    accuracy = []
    for i in range(10):
      X_train, X_test, y_train, y_test = addNoise(Sonar,n)
      train_S_noisy = pd.concat([X_train, y_train], axis =1)
      test_S_noisy = pd.concat([X_test, y_test], axis =1)

      model = Boosting(train_S_noisy,T,test_S_noisy)
      model.myfit()
      model.mypredict()
      accuracy.append(model.accuracy[-1])

    print('\t\t\tAccuracy for T =' ,T ,': %.2f %%' %(np.mean(accuracy)*100) )
# -*- coding: utf-8 -*-
"""ML_HW3_Bagging.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1eFP8VfDl2g6eFKV2ry5OSkcqDVCnNj_Q

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

"""# importing datasets"""

Diabetes = pd.read_csv('Diabetes.txt', header=None, sep="\t")
Diabetes = Diabetes.drop(9, axis=1)

Ionosphere = pd.read_csv('Ionosphere.txt', header=None)

Sonar = pd.read_csv('Sonar.txt', header=None)

Breast = pd.read_csv('BreastTissue.txt', header=None, sep="\t")

Glass = pd.read_csv('Glass.txt', header=None, sep="\t")
Glass = Glass.drop(10, axis=1)

Wine = pd.read_csv('Wine.txt', header=None)

"""# Splitting the datasets into the Training set and Test set"""

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(Glass.iloc[:, :-1], Glass.iloc[:, -1], test_size = 0.3, shuffle=True)

train_Glass = pd.concat([X_train, y_train], axis =1)
test_Glass = pd.concat([X_test, y_test], axis =1)

print(train_Glass, '\n')
print(test_Glass)

"""# Testing our weak learner (weak decision tree)"""

from sklearn.metrics import confusion_matrix, accuracy_score

weak_tree = DecisionTreeClassifier(criterion="entropy",max_depth=1)

X_train, X_test, y_train, y_test = train_test_split(Diabetes.iloc[:, :-1], Diabetes.iloc[:, -1], test_size = 0.3, shuffle=True)
weak_tree.fit(X_train, y_train)
y_pred = weak_tree.predict(X_test)
Diabetes_before = accuracy_score(y_test, y_pred) * 100
print("%.2f%% For Diabetese" %Diabetes_before)

weak_tree = DecisionTreeClassifier(criterion="entropy",max_depth=1)

X_train, X_test, y_train, y_test = train_test_split(Ionosphere.iloc[:, :-1], Ionosphere.iloc[:, -1], test_size = 0.3, shuffle=True)
weak_tree.fit(X_train, y_train)
y_pred = weak_tree.predict(X_test)
Ionosphere_before = accuracy_score(y_test, y_pred) * 100
print("%.2f%% For Ionosphere" %Ionosphere_before)

weak_tree = DecisionTreeClassifier(criterion="entropy",max_depth=1)

X_train, X_test, y_train, y_test = train_test_split(Sonar.iloc[:, :-1], Sonar.iloc[:, -1], test_size = 0.3, shuffle=True)
weak_tree.fit(X_train, y_train)
y_pred = weak_tree.predict(X_test)
Sonar_before = accuracy_score(y_test, y_pred) * 100
print("%.2f%% For Sonar" %Sonar_before)

weak_tree = DecisionTreeClassifier(criterion="entropy",max_depth=1)

X_train, X_test, y_train, y_test = train_test_split(Wine.iloc[:, :-1], Wine.iloc[:, -1], test_size = 0.3, shuffle=True)
weak_tree.fit(X_train, y_train)
y_pred = weak_tree.predict(X_test)
Wine_before = accuracy_score(y_test, y_pred) * 100
print("%.2f%% For Wine" %Wine_before)

weak_tree = DecisionTreeClassifier(criterion="entropy",max_depth=4)

X_train, X_test, y_train, y_test = train_test_split(Glass.iloc[:, :-1], Glass.iloc[:, -1], test_size = 0.3, shuffle=True)
weak_tree.fit(X_train, y_train)
y_pred = weak_tree.predict(X_test)
Glass_before = accuracy_score(y_test, y_pred) * 100
print("%.2f%% For Glass" %Glass_before)

weak_tree = DecisionTreeClassifier(criterion="entropy",max_depth=4)

X_train, X_test, y_train, y_test = train_test_split(Breast.iloc[:, :-1], Breast.iloc[:, -1], test_size = 0.3, shuffle=True)
weak_tree.fit(X_train, y_train)
y_pred = weak_tree.predict(X_test)
Breast_before = accuracy_score(y_test, y_pred) * 100
print("%.2f%% For Breast" %Breast_before)

"""# Functions"""

def makeSamples(dataset,T):
  samples = []
  for i in range(T):
    result = dataset.sample( frac = 1, replace = True)
    samples.append(result)

  return samples

def addNoise(dataset,n):

  X_train, X_test, y_train, y_test = train_test_split(dataset.iloc[:, :-1], dataset.iloc[:, -1], test_size = 0.3, shuffle=True)
  cols = [i for i in range(len(dataset.columns)-1)]
  list_of_random_items = random.sample(cols, math.ceil((len(dataset.columns)-1) * n/100))
  noise = X_train.iloc[:, list_of_random_items] + np.random.normal( 0,1, X_train.iloc[:, list_of_random_items].shape )
  X_train.iloc[:,list_of_random_items] = noise

  return X_train, X_test,y_train,y_test

"""# Testing"""

bagging_T = [11,21,31,41]

#Diabetes
print('\t\t  scores for Diabetes (%.2f%%' %Diabetes_before ,'before bagging)\n' )

weak_tree = DecisionTreeClassifier(criterion="entropy",max_depth=1)

for T in bagging_T:
  bagging_score = []
  for iterate in range(10):
    X_train, X_test, y_train, y_test = train_test_split(Diabetes.iloc[:, :-1], Diabetes.iloc[:, -1], test_size = 0.3, shuffle=True)
    train_Diabetes = pd.concat([X_train, y_train], axis =1)
    test_Diabetes = pd.concat([X_test, y_test], axis =1)
    samples = makeSamples(train_Diabetes, T)
    predictions = []
    for i in range(T):   
      model = weak_tree.fit(samples[i].iloc[:, :-1], samples[i].iloc[:, -1])
      predictions.append(model.predict(X_test))
      
    bagging = []
    for c in range(len(predictions[0])):
      col = [predictions[i][c] for i in range(T)]
      bagging.append(np.unique(col)[np.argmax(np.unique(col, return_counts= True)[1])])  
    bagging_score.append(accuracy_score(y_test, bagging) * 100)
  
  print('\t\t\tbagging score for T =', T , ': %.2f%%' %np.mean(bagging_score))

print('-'*90)

#Ionosphere
print('\t\t  scores for Ionosphere (%.2f%%' %Ionosphere_before ,'before bagging)\n' )

weak_tree = DecisionTreeClassifier(criterion="entropy",max_depth=1)

for T in bagging_T:
  bagging_score = []
  for iterate in range(10):
    X_train, X_test, y_train, y_test = train_test_split(Ionosphere.iloc[:, :-1], Ionosphere.iloc[:, -1], test_size = 0.3, shuffle=True)
    train_Ionosphere = pd.concat([X_train, y_train], axis =1)
    test_Ionosphere = pd.concat([X_test, y_test], axis =1)
    samples = makeSamples(train_Ionosphere, T)
    predictions = []
    for i in range(T):   
      model = weak_tree.fit(samples[i].iloc[:, :-1], samples[i].iloc[:, -1])
      predictions.append(model.predict(X_test))
      
    bagging = []
    for c in range(len(predictions[0])):
      col = [predictions[i][c] for i in range(T)]
      bagging.append(np.unique(col)[np.argmax(np.unique(col, return_counts= True)[1])])  
    bagging_score.append(accuracy_score(y_test, bagging) * 100)
  
  print('\t\t\tbagging score for T =', T , ': %.2f%%' %np.mean(bagging_score))

print('-'*90)

#Sonar
print('\t\t  scores for Sonar (%.2f%%' %Sonar_before ,'before bagging)\n' )

weak_tree = DecisionTreeClassifier(criterion="entropy",max_depth=1)

for T in bagging_T:
  bagging_score = []
  for iterate in range(10):
    X_train, X_test, y_train, y_test = train_test_split(Sonar.iloc[:, :-1], Sonar.iloc[:, -1], test_size = 0.3, shuffle=True)
    train_Sonar = pd.concat([X_train, y_train], axis =1)
    test_Sonar = pd.concat([X_test, y_test], axis =1)
    samples = makeSamples(train_Sonar, T)
    predictions = []
    for i in range(T):   
      model = weak_tree.fit(samples[i].iloc[:, :-1], samples[i].iloc[:, -1])
      predictions.append(model.predict(X_test))
      
    bagging = []
    for c in range(len(predictions[0])):
      col = [predictions[i][c] for i in range(T)]
      bagging.append(np.unique(col)[np.argmax(np.unique(col, return_counts= True)[1])])  
    bagging_score.append(accuracy_score(y_test, bagging) * 100)
  
  print('\t\t\tbagging score for T =', T , ': %.2f%%' %np.mean(bagging_score))

print('-'*90)

#Wine
print('\t\t  scores for Wine (%.2f%%' %Wine_before ,'before bagging)\n' )

weak_tree = DecisionTreeClassifier(criterion="entropy",max_depth=1)

for T in bagging_T:
  bagging_score = []
  for iterate in range(10):
    X_train, X_test, y_train, y_test = train_test_split(Wine.iloc[:, :-1], Wine.iloc[:, -1], test_size = 0.3, shuffle=True)
    train_Wine = pd.concat([X_train, y_train], axis =1)
    test_Wine = pd.concat([X_test, y_test], axis =1)
    samples = makeSamples(train_Wine, T)
    predictions = []
    for i in range(T):   
      model = weak_tree.fit(samples[i].iloc[:, :-1], samples[i].iloc[:, -1])
      predictions.append(model.predict(X_test))
      
    bagging = []
    for c in range(len(predictions[0])):
      col = [predictions[i][c] for i in range(T)]
      bagging.append(np.unique(col)[np.argmax(np.unique(col, return_counts= True)[1])])  
    bagging_score.append(accuracy_score(y_test, bagging) * 100)
  
  print('\t\t\tbagging score for T =', T , ': %.2f%%' %np.mean(bagging_score))

print('-'*90)

#Glass
print('\t\t  scores for Glass (%.2f%%' %Glass_before ,'before bagging)\n' )

weak_tree = DecisionTreeClassifier(criterion="entropy",max_depth=4)

for T in bagging_T:
  bagging_score = []
  for iterate in range(10):
    X_train, X_test, y_train, y_test = train_test_split(Glass.iloc[:, :-1], Glass.iloc[:, -1], test_size = 0.3, shuffle=True)
    train_Glass = pd.concat([X_train, y_train], axis =1)
    test_Glass = pd.concat([X_test, y_test], axis =1)
    samples = makeSamples(train_Glass, T)
    predictions = []
    for i in range(T):   
      model = weak_tree.fit(samples[i].iloc[:, :-1], samples[i].iloc[:, -1])
      predictions.append(model.predict(X_test))
      
    bagging = []
    for c in range(len(predictions[0])):
      col = [predictions[i][c] for i in range(T)]
      bagging.append(np.unique(col)[np.argmax(np.unique(col, return_counts= True)[1])])  
    bagging_score.append(accuracy_score(y_test, bagging) * 100)
  
  print('\t\t\tbagging score for T =', T , ': %.2f%%' %np.mean(bagging_score))

print('-'*90)

#Breast
print('\t\t  scores for Breast (%.2f%%' %Breast_before ,'before bagging)\n' )

weak_tree = DecisionTreeClassifier(criterion="entropy",max_depth=4)

for T in bagging_T:
  bagging_score = []
  for iterate in range(10):
    X_train, X_test, y_train, y_test = train_test_split(Breast.iloc[:, :-1], Breast.iloc[:, -1], test_size = 0.3, shuffle=True)
    train_Breast = pd.concat([X_train, y_train], axis =1)
    test_Breast = pd.concat([X_test, y_test], axis =1)
    samples = makeSamples(train_Breast, T)
    predictions = []
    for i in range(T):   
      model = weak_tree.fit(samples[i].iloc[:, :-1], samples[i].iloc[:, -1])
      predictions.append(model.predict(X_test))
      
    bagging = []
    for c in range(len(predictions[0])):
      col = [predictions[i][c] for i in range(T)]
      bagging.append(np.unique(col)[np.argmax(np.unique(col, return_counts= True)[1])])  
    bagging_score.append(accuracy_score(y_test, bagging) * 100)
  
  print('\t\t\tbagging score for T =', T , ': %.2f%%' %np.mean(bagging_score))

"""# Testing noisy data"""

Noises = [10,20,30]

#Diabetes
weak_tree = DecisionTreeClassifier(criterion="entropy",max_depth=1)

for n in Noises:
  X_train, X_test, y_train, y_test = addNoise(Diabetes,n)
  weak_tree.fit(X_train, y_train)
  predict = weak_tree.predict(X_test)
  D_before_with_noise = accuracy_score(y_test, predict) * 100

  print('\n\t\t',n,'%% Noisy scores for Diabetes (%.2f%%' %D_before_with_noise ,'before bagging)' )
  for T in bagging_T:
    bagging_score = []
    for iterate in range(10):
      X_train, X_test, y_train, y_test = addNoise(Diabetes,n)
      train_Diabetes = pd.concat([X_train, y_train], axis =1)
      test_Diabetes = pd.concat([X_test, y_test], axis =1)

      samples = makeSamples(train_Diabetes, T)
      predictions = []
      for i in range(T):   
        model = weak_tree.fit(samples[i].iloc[:, :-1], samples[i].iloc[:, -1])
        predictions.append(model.predict(X_test))
        
      bagging = []
      for c in range(len(predictions[0])):
        col = [predictions[i][c] for i in range(T)]
        bagging.append(np.unique(col)[np.argmax(np.unique(col, return_counts= True)[1])])  
      bagging_score.append(accuracy_score(y_test, bagging) * 100)
    
    print('\t\t\tbagging score for T =', T , ': %.2f%%' %np.mean(bagging_score))

print('-'*90)

#Ionosphere
weak_tree = DecisionTreeClassifier(criterion="entropy",max_depth=1)
for n in Noises:
  X_train, X_test, y_train, y_test = addNoise(Ionosphere,n)
  weak_tree.fit(X_train, y_train)
  predict = weak_tree.predict(X_test)
  I_before_with_noise = accuracy_score(y_test, predict) * 100
  print('\n\t\t',n,'%% Noisy scores for Ionosphere (%.2f%%' %I_before_with_noise ,'before bagging)' )
  for T in bagging_T:
    bagging_score = []
    for iterate in range(10):
      X_train, X_test, y_train, y_test = addNoise(Ionosphere,n) 
      train_Ionosphere = pd.concat([X_train, y_train], axis =1)
      test_Ionosphere = pd.concat([X_test, y_test], axis =1)

      samples = makeSamples(train_Ionosphere, T)
      predictions = []
      for i in range(T):   
        model = weak_tree.fit(samples[i].iloc[:, :-1], samples[i].iloc[:, -1])
        predictions.append(model.predict(X_test))
        
      bagging = []
      for c in range(len(predictions[0])):
        col = [predictions[i][c] for i in range(T)]
        bagging.append(np.unique(col)[np.argmax(np.unique(col, return_counts= True)[1])])  
      bagging_score.append(accuracy_score(y_test, bagging) * 100)
    
    print('\t\t\tbagging score for T =', T , ': %.2f%%' %np.mean(bagging_score))

print('-'*90)

#Sonar
weak_tree = DecisionTreeClassifier(criterion="entropy",max_depth=1)
for n in Noises:
  X_train, X_test, y_train, y_test = addNoise(Sonar,n)
  weak_tree.fit(X_train, y_train)
  predict = weak_tree.predict(X_test)
  S_before_with_noise = accuracy_score(y_test, predict) * 100
  print('\n\t\t',n,'%% Noisy scores for Sonar (%.2f%%' %S_before_with_noise ,'before bagging)' )
  for T in bagging_T:
    bagging_score = []
    for iterate in range(10):
      X_train, X_test, y_train, y_test = addNoise(Sonar,n)
      train_Sonar = pd.concat([X_train, y_train], axis =1)
      test_Sonar = pd.concat([X_test, y_test], axis =1)

      samples = makeSamples(train_Sonar, T)
      predictions = []
      for i in range(T):   
        model = weak_tree.fit(samples[i].iloc[:, :-1], samples[i].iloc[:, -1])
        predictions.append(model.predict(X_test))
        
      bagging = []
      for c in range(len(predictions[0])):
        col = [predictions[i][c] for i in range(T)]
        bagging.append(np.unique(col)[np.argmax(np.unique(col, return_counts= True)[1])])  
      bagging_score.append(accuracy_score(y_test, bagging) * 100)
    
    print('\t\t\tbagging score for T =', T , ': %.2f%%' %np.mean(bagging_score))

print('-'*90)

#Wine
weak_tree = DecisionTreeClassifier(criterion="entropy",max_depth=1)
for n in Noises:
  X_train, X_test, y_train, y_test = addNoise(Wine,n)
  weak_tree.fit(X_train, y_train)
  predict = weak_tree.predict(X_test)
  W_before_with_noise = accuracy_score(y_test, predict) * 100
  print('\n\t\t',n,'%% Noisy scores for Wine (%.2f%%' %W_before_with_noise ,'before bagging)' )
  for T in bagging_T:
    bagging_score = []
    for iterate in range(10):
      X_train, X_test, y_train, y_test = addNoise(Wine,n)
      train_Wine = pd.concat([X_train, y_train], axis =1)
      test_Wine = pd.concat([X_test, y_test], axis =1)

      samples = makeSamples(train_Wine, T)
      predictions = []
      for i in range(T):   
        model = weak_tree.fit(samples[i].iloc[:, :-1], samples[i].iloc[:, -1])
        predictions.append(model.predict(X_test))
        
      bagging = []
      for c in range(len(predictions[0])):
        col = [predictions[i][c] for i in range(T)]
        bagging.append(np.unique(col)[np.argmax(np.unique(col, return_counts= True)[1])])  
      bagging_score.append(accuracy_score(y_test, bagging) * 100)
    
    print('\t\t\tbagging score for T =', T , ': %.2f%%' %np.mean(bagging_score))

print('-'*90)

#Glass
weak_tree = DecisionTreeClassifier(criterion="entropy",max_depth=4)
for n in Noises:
  X_train, X_test, y_train, y_test = addNoise(Glass,n)
  weak_tree.fit(X_train, y_train)
  predict = weak_tree.predict(X_test)
  G_before_with_noise = accuracy_score(y_test, predict) * 100
  print('\n\t\t',n,'%% Noisy scores for Glass (%.2f%%' %G_before_with_noise ,'before bagging)' )
  for T in bagging_T:
    bagging_score = []
    for iterate in range(10):
      X_train, X_test, y_train, y_test = addNoise(Glass,n)
      train_Glass = pd.concat([X_train, y_train], axis =1)
      test_Glass = pd.concat([X_test, y_test], axis =1)

      samples = makeSamples(train_Glass, T)
      predictions = []
      for i in range(T):   
        model = weak_tree.fit(samples[i].iloc[:, :-1], samples[i].iloc[:, -1])
        predictions.append(model.predict(X_test))
        
      bagging = []
      for c in range(len(predictions[0])):
        col = [predictions[i][c] for i in range(T)]
        bagging.append(np.unique(col)[np.argmax(np.unique(col, return_counts= True)[1])])  
      bagging_score.append(accuracy_score(y_test, bagging) * 100)
    
    print('\t\t\tbagging score for T =', T , ': %.2f%%' %np.mean(bagging_score))

print('-'*90)

#Breast
weak_tree = DecisionTreeClassifier(criterion="entropy",max_depth=4)
for n in Noises:
  X_train, X_test, y_train, y_test = addNoise(Breast,n)
  weak_tree.fit(X_train, y_train)
  predict = weak_tree.predict(X_test)
  B_before_with_noise = accuracy_score(y_test, predict) * 100
  print('\n\t\t',n,'%% Noisy scores for Breast (%.2f%%' %B_before_with_noise ,'before bagging)' )
  for T in bagging_T:
    bagging_score = []
    for iterate in range(10):
      X_train, X_test, y_train, y_test = addNoise(Breast,n)
      train_Breast = pd.concat([X_train, y_train], axis =1)
      test_Breast = pd.concat([X_test, y_test], axis =1)

      samples = makeSamples(train_Breast, T)
      predictions = []
      for i in range(T):   
        model = weak_tree.fit(samples[i].iloc[:, :-1], samples[i].iloc[:, -1])
        predictions.append(model.predict(X_test))
        
      bagging = []
      for c in range(len(predictions[0])):
        col = [predictions[i][c] for i in range(T)]
        bagging.append(np.unique(col)[np.argmax(np.unique(col, return_counts= True)[1])])  
      bagging_score.append(accuracy_score(y_test, bagging) * 100)
    
    print('\t\t\tbagging score for T =', T , ': %.2f%%' %np.mean(bagging_score))
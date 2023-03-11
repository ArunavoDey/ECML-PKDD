# -*- coding: utf-8 -*-
"""abalationNew.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GlugHkg8pViK5sUNLGUW7p0Fjdx24mfR
"""

# Commented out IPython magic to ensure Python compatibility.
# -*- coding: utf-8 -*-
"""Final Copy of  Abalation-Final  .ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cm0xHEXXt2XLyHpQYATOVF_TYSYwOXfo
"""

#from google.colab import drive
#drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
#!pip install optuna
#!pip install shap
#!pip install seaborn
import optuna as optuna
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
import random
import os
import sys
import time
import seaborn as sns
from sklearn.metrics import accuracy_score, precision_score, recall_score, r2_score, mean_squared_error
from sklearn.model_selection import train_test_split, KFold
from tensorflow.keras import layers, losses
from tensorflow.keras.models import Model, Sequential, load_model
import tensorflow.keras as keras
import tensorflow.keras.backend as keras_backend
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.layers import Activation, Dropout, Flatten, Input, Dense, concatenate 
from sklearn.feature_selection import mutual_info_regression
from numpy import asarray
#from transfertools.models import LocIT, CBIT
import math
import scipy
from numpy import arange
from numpy.random import rand
from matplotlib import pyplot
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import matplotlib.pyplot as plt
from operator import add
#import optunann1
import optunannPOD
import subspacejsoptunaE
import xlsxwriter
from sklearn.preprocessing import StandardScaler, MinMaxScaler
#import optunanewtransformator_1
#taskArray = []
# Commented out IPython magic to ensure Python compatibility.
def top_x(df2,variable,top_x_labels):
  for label in top_x_labels:
    df2[variable+'_'+label] = np.where(df2[variable]==label,1,0)
  return df2

def converter(df1):
  df = df1
  k = 0
  for i in range(len(df.columns)):
    if df[df.columns[i]].dtypes == 'object':
      #print("String")
      uniqueValues0 = df[df.columns[i]].unique()
      title0 = df.columns[i]
      df = top_x(df, title0, uniqueValues0)
      #encoder = OneHotEncoder(handle_unknown='ignore')
      #encoder_df = pd.DataFrame(encoder.fit_transform(data[[data.columns[i]]]).toarray())
      #final_df = pd.concat([data,encoder_df],axis=1)
      #df.drop(title0, axis=1, inplace=True)
      #title0 = data.columns[i]
      #print(title0)
      #ar = {}
      #j=0
      #for s in uniqueValues0:
        #key, value = s, j+1
        #j = j+1
        #ar[key] = value
      #print(ar)
      #data = data.replace({title0: ar})
    else:
      k = k + 1
  return df



def deleter(df1):
  df = df1
  k = 0
  deleteList =[]
  for i in range(len(df.columns)):
    if df[df.columns[i]].dtypes == 'object':
      title0 = df.columns[i]
      deleteList.append(title0)  
  for i in range(len(deleteList)):
    df.drop(deleteList[i], axis=1, inplace=True)
  return df

def norm1(x, Y):
  return ((x - Y['min']) / ((Y['max']-Y['min'])+1e-60))
def normalization(x, x1):
  train_stats = x1.describe()
  train_stats = train_stats.transpose()
  return norm1(x, train_stats)

def compute_rse(y,yhat):
  #y = y.ravel()
  #yhat = yhat.ravel()
  mu = np.mean(y)
  return np.sqrt(np.sum((y-yhat)**2))/np.sqrt(np.sum((y-mu)**2))
def compute_smape(y,yhat):
  #y = y.ravel()
  #yhat = yhat.ravel()
  n = len(y)
  nr = np.abs(y - yhat)
  dr = 0.5*(np.abs(y) + np.abs(yhat))
  return (100./n)*np.sum(nr/dr)

def compute_mse(y, yhat):
  sq1 = tf.square(tf.subtract(yhat, y))
  sq1 = tf.reduce_mean(sq1)
  return sq1

if __name__ == "__main__":
  # Horovod: pin GPU to be used to process local rank (one GPU per process)
  #gpus = tf.config.experimental.list_physical_devices('GPU')
  #for gpu in gpus:
  #  tf.config.experimental.set_memory_growth(gpu, True)
  #if gpus:
  #  tf.config.experimental.set_visible_devices(gpus[hvd.local_rank()], 'GPU')
  use_msg = "Usage: " + sys.argv[0] + " input_filename"
  if len(sys.argv) < 2:
    print(use_msg)
    exit()
  #tf.debugging.set_log_device_placement(True)
  print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
  #tf.debugging.set_log_device_placement(True)
  path_to_source = sys.argv[1] #"/content/drive//MyDrive/Pascal-BFS.csv" 
  path_to_target = sys.argv[2] #"/content/drive/MyDrive/Turing-SSSP.csv"
  path_to_target2 = sys.argv[3]
  path_to_target3 = sys.argv[4]
  ep1 = int(sys.argv[5])
  trials1 = int(sys.argv[6])
  shot = sys.argv[7]
  fold = int(sys.argv[8])
  stdy = sys.argv[9]
  storageN = sys.argv[10]
  stdy2 = sys.argv[11]
  storageN2 = sys.argv[12]
  dchoice = int(sys.argv[13])
  target_domain1 = sys.argv[14]
  target_domain2 = sys.argv[15]
  target_domain3 = sys.argv[16]
  size = int(sys.argv[17])
  scaler = MinMaxScaler()
  data = pd.read_csv(path_to_source)
  dataP = pd.read_csv(path_to_target)
  dataP2 = pd.read_csv(path_to_target2)
  dataP3 = pd.read_csv(path_to_target3)
  print("data reading done")
  data = data.dropna(axis=0)
  #data = data.loc[data['ts']>1000]
  #data = data.loc[data['ts']<10000]
  #data['ts'] = np.log(data['ts'])
  dataP = dataP.dropna(axis=0)
  dataP2 = dataP2.dropna(axis=0)
  dataP3 = dataP3.dropna(axis=0)
  """  
  tm = "kernel_time"
  data[tm] = np.log(data[tm])
  dataP[tm] = np.log(dataP[tm])
  dataP2[tm] = np.log(dataP2[tm])
  dataP3[tm] = np.log(dataP3[tm])
  """
  data = data.drop("graph_name",axis =1)
  dataP = dataP.drop("graph_name",axis =1)
  dataP2 = dataP2.drop("graph_name",axis =1)
  dataP3 = dataP3.drop("graph_name",axis=1)
  data = data.drop("d2h_time",axis =1)
  dataP = dataP.drop("d2h_time",axis =1)
  dataP2 = dataP2.drop("d2h_time",axis =1)
  dataP3 = dataP3.drop("d2h_time", axis=1)
  
 
  if dchoice==0:
    data = data.drop("h2d_time",axis =1)
    dataP2 = dataP2.drop("h2d_time",axis =1)
    dataP3 = dataP3.drop("h2d_time",axis =1)
  elif dchoice==1:
    data = data.drop("h2d_time",axis =1)
    dataP = dataP.drop("h2d_time",axis =1)
    dataP3 = dataP3.drop("h2d_time",axis =1)
  else:
    dataP2 = dataP2.drop("h2d_time", axis =1)
    dataP = dataP.drop("h2d_time",axis =1)
    dataP3 = dataP3.drop("h2d_time",axis =1)
  
 
  data = data.loc[data['kernel_time']>0]
  dataP = dataP.loc[dataP['kernel_time']>0]
  dataP2 = dataP2.loc[dataP2['kernel_time']>0]
  dataP3 = dataP3.loc[dataP3['kernel_time']>0]
  data = data.loc[data['kernel_time']<1]
  dataP = dataP.loc[dataP['kernel_time']<1]
  dataP2 = dataP2.loc[dataP2['kernel_time']<1]
  dataP3 = dataP3.loc[dataP3['kernel_time']<1]
  
  tm = "kernel_time"
  data[tm] = np.log(data[tm])
  dataP[tm] = np.log(dataP[tm])
  dataP2[tm] = np.log(dataP2[tm])
  dataP3[tm] = np.log(dataP3[tm])


  data_c = converter(data)
  data2_c = converter(dataP)
  data3_c = converter(dataP2)
  data4_c = converter(dataP3)
  data_c = deleter(data_c)
  
  data2_c = deleter(data2_c)
  data3_c = deleter(data3_c)
  data4_c = deleter(data4_c)
  targetMetric1 = "kernel_time"
  targetMetric2 = "kernel_time"
  targetMetric3 = "kernel_time"
  targetMetric4 = "kernel_time"
  
  data_c = data_c.reset_index(drop=True)
  data2_c = data2_c.reset_index(drop=True)
  data3_c = data3_c.reset_index(drop=True)
  data4_c = data4_c.reset_index(drop=True)
 
  #targetMetric1 = "ts"
  Lb = data_c[targetMetric1]
  lb = data2_c[targetMetric2]
  mb = data3_c[targetMetric3]
  nb = data4_c[targetMetric4]
  data_c= data_c.drop(targetMetric1,axis =1)
  data2_c= data2_c.drop(targetMetric2,axis =1)
  data3_c= data3_c.drop(targetMetric3,axis =1)
  data4_c= data4_c.drop(targetMetric4,axis =1)
  normalized_data = scaler.fit_transform(data_c)
  normalized_data2 = scaler.transform(data2_c)
  normalized_data3 = scaler.transform(data3_c)
  normalized_data4 = scaler.transform(data4_c)
  X = normalized_data
  Y = Lb
  x = normalized_data2
  y = lb
  M = normalized_data3
  m = mb
  N = normalized_data4
  n = nb
  print("Data pre processing done")
  #dataset = (tf.data.Dataset.from_tensor_slices((tf.cast(X, tf.float64), tf.cast(Y, tf.float64) )) )
  #dataset = dataset.repeat().shuffle(10000).batch(128)
  try:
    with tf.device('/gpu:0'):
      X1 = tf.convert_to_tensor(X, dtype = tf.float64)
      
      x1 = tf.convert_to_tensor(x, dtype = tf.float64)
      xm = tf.convert_to_tensor(M, dtype = tf.float64)
      xn = tf.convert_to_tensor(N, dtype = tf.float64)
      
      Lb1= tf.convert_to_tensor(Lb, dtype = tf.float64)
      
      lb1= tf.convert_to_tensor(lb, dtype = tf.float64)
      lbm= tf.convert_to_tensor(mb, dtype = tf.float64)
      lbn= tf.convert_to_tensor(nb, dtype = tf.float64)
      
      workbook = xlsxwriter.Workbook(f"/home1/08389/hcs77/{shot}-Results-with-subspace-1.xlsx")
      worksheet = workbook.add_worksheet()
      row = 0
      col = 0
      """
      nnparameters = optunannPOD.finder(X1, Lb1, epochs= ep1, checkpoint_path=f"/home1/08389/hcs77/{shot}/", num_of_trials=trials1, fold=10, stname=stdy, storageName = storageN)  #/content/MyDrive/SimpleNN/
      print("Neurons ")
      worksheet.write(row, col, nnparameters.params['neuron'])
      print(nnparameters.params['neuron'])
      print("Number of layers")
      worksheet.write(row, col+1, nnparameters.params['num_layers'])
      print(nnparameters.params['num_layers'])
      print("Learning rate")
      worksheet.write(row, col+2, nnparameters.params['lr2'])
      print(nnparameters.params['lr2'])
      print("Best Trial Number")
      worksheet.write(row, col+3, nnparameters.number)
      print(nnparameters.number)
      
      predictorModel = optunannPOD.create_model(neurons_input= int(nnparameters.params['neuron']), num_of_layers_1=int(nnparameters.params['num_layers']), lr= float(nnparameters.params['lr2']), actF="relu", lossF="mean_squared_error")
      """
      #predictorModel = optunannPOD.create_model(neurons_input= nuron_num, num_of_layers_1= num_layers, lr= lr_rate, actF="relu", lossF="mean_squared_error")
      #predictorModel.load_weights(f"/home1/08389/hcs77/{shot}/Trial-{nnparameters.number}-model")
      #predictorModel.layers[0].trainable = False
      #predictorModel.layers[1].trainable = False
      #results = open(f"/home1/08389/hcs77/Regressor-{shot}-results.txt", "a")
      #predictorModel.fit(X1, Lb1, epochs=1000)
      #predictorModel.save_weights(f"/home1/08389/hcs77/FAMDR/{shot}-model")
      #predictions = predictorModel.predict(X1)
      #model3, mse, mae, mape = kfoldValidation(model2, newX6, Lb1, 10, 100, 384)
      #model4, testMSE, testMAE, testMAPE = kfoldTesting(predictorModel, newx6, lb1, 10, 100, 384)
      
      print("1st target")
      #size = 5
      f = open(f"/home1/08389/hcs77/{shot}-{target_domain1}-indices.txt", "r")
      nums = f.readlines()
      index =0
      while size <= 25:
        for pos in range(3):
          col = 0
          worksheet.write(row, col, shot)
          worksheet.write(row, col + 1, target_domain1)
          worksheet.write(row, col + 2, size)
          worksheet.write(row, col + 3, pos)
          #row += 1
          #predictorModel = optunannPOD.create_model(neurons_input= nuron_num, num_of_layers_1= num_layers, lr= lr_rate, actF="relu", lossF="mean_squared_error")
          #predictorModel.load_weights(f"/home1/08389/hcs77/{shot}/Trial-{trial_num}-model")
          #predictorModel.load_weights(f"/home1/08389/hcs77/CCGrid/{shot}-model ")
       
          #predictorModel.layers[0].trainable = False
          #predictorModel.layers[1].trainable = False       
          print("x1 len")
          print(len(x1))
          x2 =[]
          lb2 = []
          dropIndices = []
          line = nums[index]
          #print("lines")
          #print(line)
          #print(x1.shape)
          # = data.dropna(axis=0)
          indices = line.split()
          for i in range(size):
            rI = int(indices[i])
            print("rI")
            print(rI)
            if tf.math.count_nonzero(x1[rI:rI+1])>0:
              x2.append(x1[rI:rI+1])
              lb2.append(lb1[rI:rI+1])
              dropIndices.append(rI)
          print("before x2")
          print(len(x2))
          x2 = tf.convert_to_tensor( x2, dtype=tf.float64)
          lb2 = tf.convert_to_tensor( lb2, dtype=tf.float64)
          x2 = tf.reshape(x2, (x2.shape[0], x2.shape[2]))
          lb2 = tf.reshape(lb2, lb2.shape[0])

          #predictorModel.fit(x2, lb2, epochs=50)
          
          td2 = data2_c.drop(labels=dropIndices, axis=0)
          tx = scaler.transform(td2)
          tx1 = tf.convert_to_tensor(tx, dtype = tf.float64)
          tlb = lb.drop(labels=dropIndices, axis=0)
          tlb1 = tf.convert_to_tensor(tlb, dtype = tf.float64)
          
          
          subspace_representation6 = subspacejsoptunaE.finder(X1, x2, Lb1, lb2, epochs=ep1, checkpoint_path=f"/home1/08389/hcs77/subspace/{target_domain1}/{size}/{pos}/", num_of_trials=trials1, log_stepsP= 0, stname=f"{stdy}-{size}-{pos}", storageName = storageN)        
          model = subspacejsoptunaE.Autoencoder(intermediate_dim=X1.shape[1], original_dim1=X1.shape[1], original_dim2=x2.shape[1], numOfLayers=subspace_representation6.params["num_layers"],neurons=subspace_representation6.params["neuron"], activation="relu")
          model.load_weights(f"/home1/08389/hcs77/subspace/{target_domain1}/{size}/{pos}/Loss Type-0-Trial-{subspace_representation6.number}-model")
          newX6 = model.getEncoded1(X1)
          newx6 = model.getEncoded2(tx1)
        
          nnparameters = optunannPOD.finder(newX6, Lb1, epochs= ep1, checkpoint_path=f"/home1/08389/hcs77/waste/", num_of_trials=trials1, fold=10, stname=f"{stdy2}-{size}-{pos}", storageName = storageN2)
          predictorModel = optunannPOD.create_model(neurons_input= int(nnparameters.params['neuron']), num_of_layers_1=int(nnparameters.params['num_layers']), lr= float(nnparameters.params['lr2']), actF="relu", lossF="mean_squared_error")
          predictorModel.fit(newX6, Lb1, epochs=1000, verbose=0)
          
         

          pred = predictorModel.predict(newx6)
          testMSE = mean_squared_error(tlb1, pred)
          testRSE = compute_rse(tlb1, pred)
          testSMAPE = compute_smape(tlb1, pred)
          print(f"{target_domain1}  mse is {testMSE}")
          print(f"{target_domain1} rse is {testRSE}")
          print(f"{target_domain1} smape is  {testSMAPE}")
          worksheet.write(row, col + 4, testMSE)
          worksheet.write(row, col + 5, testRSE)
          #worksheet.write(row, col + 6, testSMAPE)
          plt.figure(figsize=(10,10))
          plt.scatter(tlb1, pred)
          plt.savefig(f"/home1/08389/hcs77/{shot}-{target_domain1}-{size}-shot-{pos}-subspace.pdf")
          row = row + 1
          index = index +1 
        size = size + 5
      f.close()
      
      """
      print("2nd target")
      size = 5
      f = open(f"/home1/08389/hcs77/{shot}-{target_domain2}-indices.txt", "r")
      nums = f.readlines()
      index =0

      while size <= 15:
        for pos in range(3):
          col = 0
          worksheet.write(row, col, shot)
          worksheet.write(row, col + 1, target_domain2)
          worksheet.write(row, col + 2, size)
          worksheet.write(row, col + 3, pos)
          #predictorModel = optunannPOD.create_model(neurons_input= nuron_num, num_of_layers_1= num_layers, lr= lr_rate, actF="relu", lossF="mean_squared_error")
          #predictorModel.load_weights(f"/home1/08389/hcs77/{shot}/Trial-{trial_num}-model")
          #predictorModel.load_weights(f"/home1/08389/hcs77/CCGrid/{shot}-model ")
          #predictorModel.layers[0].trainable = False
          #predictorModel.layers[1].trainable = False
 
              


          x3 =[]
          lb3 = []
          dropIndices = []
          line = nums[index]
          #print("lines")
          #print(line)
          #print(x1.shape)
          # = data.dropna(axis=0)
          indices = line.split()
          for i in range(size):
            rI = int(indices[i])
            if tf.math.count_nonzero(xm[rI:rI+1])>0:
              x3.append(xm[rI:rI+1])
              lb3.append(lbm[rI:rI+1])
              dropIndices.append(rI)
          #print("before x2")
          #print(x2)
          x3 = tf.convert_to_tensor( x3, dtype=tf.float64)
          lb3 = tf.convert_to_tensor( lb3, dtype=tf.float64)
          x3 = tf.reshape(x3, (x3.shape[0], x3.shape[2]))
          lb3 = tf.reshape(lb3, lb3.shape[0])
          
          #predictorModel.fit(x3, lb3, epochs=50)
          
          td3 = data3_c.drop(labels=dropIndices, axis=0)
          tx3 = scaler.transform(td3)
          tx3 = tf.convert_to_tensor(tx3, dtype = tf.float64)
          tlb3 = mb.drop(labels=dropIndices, axis=0)
          tlb3 = tf.convert_to_tensor(tlb3, dtype = tf.float64)
           
          subspace_representation6 = subspacejsoptunaE.finder(X1, x3, Lb1, lb3, epochs=ep1, checkpoint_path=f"/home1/08389/hcs77/subspace/{target_domain2}/{size}/{pos}/", num_of_trials=trials1, log_stepsP=lossType, stname=stdy, storageName = storageN )
          model = subspacejsoptunaE.Autoencoder(intermediate_dim=X1.shape[1], original_dim1=X1.shape[1], original_dim2=x3.shape[1], numOfLayers=subspace_representation6.params["num_layers"],neurons=subspace_representation6.params["neuron"], activation="relu")
          model.load_weights(f"/home1/08389/hcs77/subspace/{target_domain2}/{size}/{pos}/Loss Type-{lossType}-Trial-{subspace_representation6.number}-model")
          newX6 = model.getEncoded1(X1)
          newx6 = model.getEncoded2t(tx3)

          nnparameters = optunannPOD.finder(newX6, Lb1, epochs= ep1, checkpoint_path=f"/home1/08389/hcs77/waste/", num_of_trials=trials1, fold=10, stname=stdy, storageName = storageN)
          predictorModel = optunannPOD.create_model(neurons_input= int(nnparameters.params['neuron']), num_of_layers_1=int(nnparameters.params['num_layers']), lr= float(nnparameters.params['lr2']), actF="relu", lossF="mean_squared_error")
          predictorModel.fit(newX6, Lb1, epochs=1000)


          pred2 = predictorModel.predict(newx6)
          testMSE2 = mean_squared_error(tlb3, pred2)
          testRSE2 = compute_rse(tlb3, pred2)
          testSMAPE2 = compute_smape(tlb3, pred2)
          print(f"{target_domain2} mse is {testMSE2}")
          print(f"{target_domain2} rse is {testRSE2}")
          print(f"{target_domain2} smape is {testSMAPE2}")
          worksheet.write(row, col + 4, testMSE2)
          worksheet.write(row, col + 5, testRSE2)
          worksheet.write(row, col + 6, testSMAPE2)
          plt.figure(figsize=(10,10))
          plt.scatter(tlb3, pred2)
          plt.savefig(f"/home1/08389/hcs77/{shot}-{target_domain2}-{size}-shot-{pos}.pdf")
          row = row + 1
          index = index + 1
        size = size + 5
      f.close()
      
      """
      """
      print("3rd target")
      size = 5
      f = open(f"/home1/08389/hcs77/{shot}-{target_domain3}-indices.txt", "r")
      nums = f.readlines()
      index =0
      while size <= 15:
        for pos in range(3):
          col = 0
          worksheet.write(row, col, shot)
          worksheet.write(row, col + 1, target_domain3)
          worksheet.write(row, col + 2, size)
          worksheet.write(row, col + 3, pos)
          #predictorModel = optunannPOD.create_model(neurons_input= nuron_num, num_of_layers_1= num_layers, lr= lr_rate, actF="relu", lossF="mean_squared_error")
          #predictorModel.load_weights(f"/home1/08389/hcs77/{shot}/Trial-{trial_num}-model")
          #predictorModel.load_weights(f"/home1/08389/hcs77/CCGrid/{shot}-model ")
          #predictorModel.layers[0].trainable = False
          #predictorModel.layers[1].trainable = False
          
          
          x4 =[]
          lb4 = []
          dropIndices = []
          line = nums[index]
          #print("lines")
          #print(line)
          #print(x1.shape)
          # = data.dropna(axis=0)
          indices = line.split()
          for i in range(size):
            rI = int(indices[i])
            if tf.math.count_nonzero(xn[rI:rI+1])>0:
              x4.append(xn[rI:rI+1])
              lb4.append(lbn[rI:rI+1])
              dropIndices.append(rI)
          #print("before x2")
          #print(x2)
          x4 = tf.convert_to_tensor( x4, dtype=tf.float64)
          lb4 = tf.convert_to_tensor( lb4, dtype=tf.float64)
          x4 = tf.reshape(x4, (x4.shape[0], x4.shape[2]))
          lb4 = tf.reshape(lb4, lb4.shape[0])



          predictorModel.fit(x4, lb4, epochs=50)
          
          td4 = data4_c.drop(labels=dropIndices, axis=0)
          tx4 = scaler.transform(td4)
          tx4 = tf.convert_to_tensor(tx4, dtype = tf.float64)
          tlb4 = nb.drop(labels=dropIndices, axis=0)
          tlbn = tf.convert_to_tensor(tlb4, dtype = tf.float64)
          

          subspace_representation6 = subspacejsoptunaE.finder(X1, x4, Lb1, lb4, epochs=ep1, checkpoint_path=f"/home1/08389/hcs77/subspace/{target_domain3}/{size}/{pos}/", num_of_trials=trials1, log_stepsP=lossType, stname=stdy, storageName = storageN)
          model = subspacejsoptunaE.Autoencoder(intermediate_dim=X1.shape[1], original_dim1=X1.shape[1], original_dim2=x4.shape[1], numOfLayers=subspace_representation6.params["num_layers"],neurons=subspace_representation6.params["neuron"], activation="relu")
          model.load_weights(f"/home1/08389/hcs77/subspace/{target_domain3}/{size}/{pos}/Loss Type-{lossType}-Trial-{subspace_representation6.number}-model")
          newX6 = model.getEncoded1(X1)
          newx6 = model.getEncoded2t(tx4)

          nnparameters = optunannPOD.finder(newX6, Lb1, epochs= ep1, checkpoint_path=f"/home1/08389/hcs77/waste/", num_of_trials=trials1, fold=10, stname=stdy2, storageName = storageN2)
          predictorModel = optunannPOD.create_model(neurons_input= int(nnparameters.params['neuron']), num_of_layers_1=int(nnparameters.params['num_layers']), lr= float(nnparameters.params['lr2']), actF="relu", lossF="mean_squared_error")
          predictorModel.fit(newX6, Lb1, epochs=1000)



          pred3 = predictorModel.predict(newx6)
          testMSE3 = mean_squared_error(tlbn, pred3)
          testRSE3 = compute_rse(tlbn, pred3)
          testSMAPE3 = compute_smape(tlbn, pred3)
          print(f"{target_domain3} mse is {testMSE3}")
          print(f"{target_domain3} rse is {testRSE3}")
          print(f"{target_domain3} smape is {testSMAPE3}")
          worksheet.write(row, col + 4, testMSE3)
          worksheet.write(row, col + 5, testRSE3)
          worksheet.write(row, col + 6, testSMAPE3)
          plt.figure(figsize=(10,10))
          plt.scatter(tlbn, pred3)
          plt.savefig(f"/home1/08389/hcs77/{shot}-{target_domain3}-{size}-shot-{pos}.pdf")
          row = row + 1
          index = index + 1
        size = size + 5
      f.close()
      """
      #pred3 = predictorModel.predict(xn)
      #mse = mean_squared_error(Lb1, predictions)
      #rse = compute_rse(Lb1, predictions)
      #smape = compute_smape(Lb1, predictions)
      #testMSE = compute_mse(pred, lb1)
      """
      testMSE = mean_squared_error(lb1, pred)
      testRSE = compute_rse(lb1, pred)
      testSMAPE = compute_smape(lb1, pred)
      testMSE2 = mean_squared_error(lbm, pred2)
      testRSE2 = compute_rse(lbm, pred2)
      testSMAPE2 = compute_smape(lbm, pred2)
      testMSE3 = mean_squared_error(lbn, pred3)
      testRSE3 = compute_rse(lbn, pred3)
      testSMAPE3 = compute_smape(lbn, pred3)
      """
      #print(f"Best trial number is {nnparameters.number}")
      #print(f"Source mse is {mse}")
      #print(f"Source mse is {rse}")
      #print(f"Source mse is {smape}")
      """
      print(f"Target mse is {testMSE}")
      print(f"Target rse is {testRSE}")
      print(f"Target smape is  {testSMAPE}")
      print(f"2nd target mse is {testMSE2}")
      print(f"2nd target rse is {testRSE2}")
      print(f"2nd target smape is {testSMAPE2}")
      print(f"3rd target mse is {testMSE3}")
      print(f"3rd target rse is {testRSE3}")
      print(f"3rd target smape is {testSMAPE3}")
      """
      
      #plt.figure(figsize=(10,10))
      #plt.scatter(Lb1, predictions)
      #plt.savefig(f"/home1/08389/hcs77/Source-{shot}-2.pdf")
      """
      plt.figure(figsize=(10,10))
      plt.scatter(lb1, pred)
      plt.savefig(f"/home1/08389/hcs77/target1-{shot}.pdf")
      plt.figure(figsize=(10,10))
      plt.scatter(lbm, pred2)
      plt.savefig(f"/home1/08389/hcs77/target2-{shot}.pdf")
      plt.figure(figsize=(10,10))
      plt.scatter(lbn, pred3)
      plt.savefig(f"/home1/08389/hcs77/target3-{shot}.pdf")
      """
      workbook.close()
    #print(f"Best trial number is {subspace_representation6.number}")
    #print(f"Source mse is {np.mean(mse)}")
    #print(f"Target mse is {np.mean(testMSE)}")
    
  except RuntimeError as e:
    print(e)

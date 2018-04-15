import pandas as pd
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.externals import joblib
import lambdathreshold as lmb
import problib as pl
import numpy as np

def b2d(x):
	return int(x.replace('"',''),2)

def parse2df(filename,names):
	dataset = pd.read_csv(filename, names=names)
	dataset= dataset.ix[1:]
	dataset=dataset.drop('Sent',1)
	dataset=dataset.drop('Received',1)
	#print dataset.describe()
	return dataset


#train files
#0.2
#~ "./simresults/training_set/llrsgndict-1024-0p2-18-02-15_14-58-44.txt
#~ "./simresults/training_set/llrsgndict-1024-0p2-On-0p2-18-02-15_14-58-44.csv
#~ "./simresults/training_set/llrsgndict-1024-0p2-On-0p25-18-02-15_14-58-44.csv
#0.04
#~ "./simresults/training_set/llrsgndict-1024-0p04-18-02-15_14-58-19.txt
#~ "./simresults/training_set/llrsgndict-1024-0p04-On-0p2-18-02-15_14-58-19.csv
#~ "./simresults/training_set/llrsgndict-1024-0p04-On-0p04-18-02-15_14-58-19.csv
#~ "./simresults/training_set/llrsgndict-1024-0p04-On-0p15-18-02-15_14-58-19.csv
#~ "./simresults/training_set/llrsgndict-1024-0p04-On-0p25-18-02-15_14-58-19.csv
#0.15
#~ "./simresults/training_set/llrsgndict-1024-0p15-18-02-15_14-58-32.txt
#~ "./simresults/training_set/llrsgndict-1024-0p15-On-0p2-18-02-15_14-58-32.csv
#~ "./simresults/training_set/llrsgndict-1024-0p15-On-0p15-18-02-15_14-58-32.csv
#~ "./simresults/training_set/llrsgndict-1024-0p15-On-0p25-18-02-15_14-58-32.csv


N=1024
runsim=1000
channel_plist=[0.04,0.15,0.2,0.25]
train_plist=channel_plist[:-1]
train_plist=[0.2]

#LLRdict structure
names = ["LLR"+str(i) for i in range(N)]
dtypes={}
for n in names:
	dtypes[n]=float
	
names.extend(["Sent","Received"])
dtypes["Sent"]=object
dtypes["Received"]=object


# Training dataset
tfile={}
tfile["0.04"]=["./simresults/training_set/llrsgndict-1024-0p04-On-0p04-18-02-15_14-58-19.csv",
 "./simresults/training_set/llrsgndict-1024-0p04-On-0p15-18-02-15_14-58-19.csv",
 "./simresults/training_set/llrsgndict-1024-0p04-On-0p2-18-02-15_14-58-19.csv",
"./simresults/training_set/llrsgndict-1024-0p04-On-0p25-18-02-15_14-58-19.csv"]
tfile["0.15"]=["./simresults/training_set/llrsgndict-1024-0p15-On-0p15-18-02-15_14-58-32.csv",
"./simresults/training_set/llrsgndict-1024-0p15-On-0p2-18-02-15_14-58-32.csv",
"./simresults/training_set/llrsgndict-1024-0p15-On-0p25-18-02-15_14-58-32.csv"]
tfile["0.2"]=["./simresults/training_set/llrsgndict-1024-0p2-On-0p2-18-02-15_14-58-44.csv",
"./simresults/training_set/llrsgndict-1024-0p2-On-0p25-18-02-15_14-58-44.csv"]


seed = 7
scoring = 'accuracy'
# Spot Check Algorithms
models = []
models.append(('LR', LogisticRegression()))
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC()))


h0=[0]*runsim
h1x=[1]*runsim

results = []
modnames = []
#training 
for design_p in train_plist:
	des_p=str(design_p)
	print "Design_for:"+des_p+"\n"
	frames=[parse2df(channel_pfile,names) for channel_pfile in tfile[des_p]]
	trainingdata=pd.concat(frames)
	h=list(h0)
	h1=h1x*(len(tfile[des_p])-1)
	h.extend(h1)
	trainingdata=trainingdata.assign(Hypothesis=h)
	trainingdata=trainingdata.sample(n=1000)
	array = trainingdata.values
	X = array[:,0:1023]
	Y = array[:,1024]
	Y=Y.astype('int')
	print X
	print Y
	for name, model in models:
		kfold = model_selection.KFold(n_splits=10, random_state=seed)
		cv_results = model_selection.cross_val_score(model, X, Y, cv=kfold, scoring=scoring)
		results.append(cv_results)
		modnames.append(name)
		msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
		print(msg)

	

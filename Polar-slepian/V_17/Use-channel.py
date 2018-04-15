import pandas
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
import lambdathreshold as lmb

# validation dataset
vfile={}
vfile["0.04"]="./simresults/validation_set/llrsgndict-1024-0p04-18-03-14_00-28-11.txt"
vfile["0.15"]="./simresults/validation_set/llrsgndict-1024-0p15-18-03-14_00-28-09.txt"
vfile["0.2"]="./simresults/validation_set/llrsgndict-1024-0p2-18-03-14_00-28-04.txt"

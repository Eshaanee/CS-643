import sys
import pickle

from numpy import array
from pyspark import SparkContext, SparkConf

from pyspark.mllib.linalg import Vectors
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.classification import LogisticRegressionWithSGD
from pyspark.mllib.classification import LogisticRegressionWithLBFGS
from pyspark.mllib.classification import SVMWithSGD
from pyspark.mllib.classification import NaiveBayes
from pyspark.mllib.tree import DecisionTree, DecisionTreeModel
from pyspark.mllib.tree import RandomForest
from pyspark.mllib.util import MLUtils
from pyspark.mllib.evaluation import MulticlassMetrics

trainDataPath = "s3://cloudpa2/TrainingDataset.csv"
valDataPath = "s3://cloudpa2/ValidationDataset.csv"

sc = SparkContext.getOrCreate();
sc.getConf().setAppName('cloudpa2')

rawData = sc.textFile(trainDataPath)
records = rawData.filter(lambda str: "\"" not in str).map(lambda str: str.split(";")).map( lambda strVal : [float(x) for x in strVal]) 
data = records.map(lambda arr : LabeledPoint(int(arr[-1]) - 1, Vectors.dense(arr[:-1])))

valRawData = sc.textFile(valDataPath)
valRecords = valRawData.filter(lambda str: "\"" not in str).map(lambda str: str.split(";")).map( lambda strVal : [float(x) for x in strVal]) 
valData = valRecords.map(lambda arr: (arr[:-1], int(arr[-1]) - 1))

rfModel = RandomForest.trainClassifier(data, numClasses=10, categoricalFeaturesInfo={}, numTrees=100)
rfModelPredictionAndLabels = rfModel.predict(valData.map(lambda tp : tp[0])).zip(valData.map(lambda _: float(_[1])))

rfModelMetric = MulticlassMetrics(rfModelPredictionAndLabels)
print("F1Score : %s"%(rfModelMetric.accuracy))

rfModel.save(sc, "s3://myprogrambucket123/rfwine_model.model")

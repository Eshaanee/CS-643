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
from pyspark.mllib.tree import RandomForestModel
from pyspark.mllib.util import MLUtils
from pyspark.mllib.evaluation import MulticlassMetrics
import sys

if(len(sys.argv) < 3):
    print("Usage : testfilePath")
    sys.exit(-1)


modelPath=sys.argv[1]
valDataPath=sys.argv[2]


#trainDataPath = "s3://cloudpa2/TrainingDataset.csv"
#valDataPath = "s3://cloudpa2/ValidationDataset.csv"


sc = SparkContext.getOrCreate();
sc.getConf().setAppName('cs-643')

valRawData = sc.textFile(valDataPath)
valRecords = valRawData.filter(lambda str: "\"" not in str).map(lambda str: str.split(";")).map( lambda strVal : [float(x) for x in strVal]) 
valData = valRecords.map(lambda arr: (arr[:-1], int(arr[-1]) - 1))

rf=RandomForestModel.load(sc,modelPath)

rfModelPredictionAndLabels = rf.predict(valData.map(lambda tp : tp[0])).zip(valData.map(lambda _: float(_[1])))
rfModelMetric = MulticlassMetrics(rfModelPredictionAndLabels)


print("F1Score : %s"%(rfModelMetric.accuracy))


#print("F1Score : %s"%(rfModelMetric.fMeasure(4.0,3.0)))


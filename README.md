# CS-643 Assignment 2
To run on EMR cluster without docker :

Create a s3 bucket named myprogrambucket123</br>
upload ValidationDataset.csv, TrainingDataset.csv , testerD115.py and trainerD115.py in it</br>
aws s3 cp s3://myprogrambucket123/TrainingDataset.csv ~ #to copy csv file from s3 to emr
aws s3 cp s3://myprogrambucket123/ValidationDataset.csv ~

spark submit trainerD115.py #saves the model in the s3 bucket

in current folder use command (to download model that was uploaded by trainerD115.py from s3 bucket if not present) :

aws s3 cp s3://myprogrambucket123/ . --recursive

Format : spark-submit testerD115.py #to run testerD115.py
eg : spark-submit testerD115.py


For Docker :
Download spark 3.0 tar and untar it in "spark" folder in the current directory.

sudo docker build -t ishani/cs_643_proj

sudo docker run -v /root/ishani/ValidationDataset.csv:/root/ishani/ValidationDataset.csv  ishani/cs_643_proj /root/ishani/ValidationDataset.csv

docker pull ishani/cs_643_proj:latest

Docker Image : https://hub.docker.com/layers/eshaanee123/cs_643_proj/latest/images/sha256-57251f55a75a0d4b749b10982379a3f06bdd9be997ef6543c81ca6722fbe517e?context=explore

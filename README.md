# Aalto-OperatingSystems-Challenge

Repository for the voluntary Challenge Exercise in the Master's course "Operating Systems".

## 0. TODO
- create a dockerfile with the container
- add tutorials for dockerfile
- update installation instructions


## 1. Install docker

As host environment for the docker container Ubuntu 16.04 LTS (64 Bit) was used. To install docker execute this on the Ubuntu host machine:
```shell
sudo apt-get update
sudo apt-get install linux-image-extra-$(uname -r) linux-image-extra-virtual
sudo apt-get install apt-transport-https ca-certificates curl software-properties-common
```
Add the docker PGP key to the host machine:
```shell
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
```
Finally install docker:
```shell
sudo apt-get update
sudo apt-get install docker-ce
```
To verify the installation run:
```shell
sudo docker run hello-world
```
sources: https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/


## 2. Using the docker image
The docker container as can be found in //TODO link and was exported using:
```shell
sudo docker export [container name] | gzip car_detector.tar.gz
```
It can be downloaded from https://1drv.ms/u/s!Aoi3Wc_cMCrSsfpj5Ldlzqb5U39-tg and imported/reused with docker using:
```shell
sudo docker import
```

## 3. Manual installation
### a) Using a docker image with tensorflow binaries
#### Execute the following commands on the host system to start a docker container with CPU support only and connect via bash:
```shell
docker run -it -p hostPort:containerPort gcr.io/tensorflow/tensorflow:latest-devel bash
```
An existing machine can be resumed and accessed with:
```shell
sudo docker start [machine name]
sudo docker attach [machine name]
```
The machine name can be found using:
```shell
sudo docker ps -a
```
#### GPU support TODO


### b) Install additional TensorFlow functions and the object detection api in the container

#### Install additional libraries in the container using bash access
```shell
sudo apt-get install protobuf-compiler python-pil python-lxml
sudo pip install jupyter
sudo pip install pillow
sudo pip install lxml
sudo pip install matplotlib
```

### c) Install the object detection API

Clone into: 
```shell
git clone https://github.com/tensorflow/models.git
```
Download the files. The folder does not matter but for the dockerfile the models folder is in /tensorflow/tensorflow/models

#### Install Protbuf Compiler in the container
Check for latest protoc version with:
```shell
protoc --version
```
If it is not the latest version download it from the following link for python and build it with:
Download: https://github.com/google/protobuf/releases
```shell
./configure
make check
make install
```
Execute in the tensorflow/models/research directory:
```shell
protoc object\_detection/protos/*.proto --python_out=.
```
#### Add Libraries to Pythonpath
Run this command in every terminal started or add them to your ~/.bashrc
```shell
export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim
```
#### Verify the installation
```shell
python object_detection/builders/model_builder_test.py
```
source: https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/installation.md

## 4. Usage
To edit and run the jupyter notebook navigate in the container to the /tensorflow/models/research/object_detection/ folder and run the notebook server with:
```shell
jupyter notebook --allow-root
```
Or just run the python script in the same folder with:
```shell
python car_detector.py
```

Once started the container starts collection image data from the web address http://tpark-cam.cs.aalto.fi/ which is used for demonstration purposes. The script can also be altered to use locally saved images and a further improvement for the image acquisition could be, instead of downloading, to push image data to the tensor flow program.

TensorFlow is then using the Object Detection API to find objects in the received image. Due to the bad quality of the demo image stream the sensitivity of the system was set to a value of 0.3 which means that objects that are 40% or more likely to be a car will be counted.

The metadata (amount of cars, array with their positions in the image, and probability for each car to actually be a car) is then sent to the data handler.

The data handler is saving the data in a database and provides an interface for an application or a user to get the data from there using HTTP.

## The Data Handler

The repository with the implementation of the data handler can be found here: https://github.com/cell2749/ImageProcessingDataHandler

The data handler consists of one or more dyno (https://devcenter.heroku.com/articles/dynos) containers running in a heroku (https://www.heroku.com/) web application. This allows the data handling to be scaled to whatever needs the application has.
The metadata coming from the tensor flow docker containers is sent to the handler using the POST request method. The metadata is saved in a Mongo database and can be queried using HTTP and a Node JS interface.









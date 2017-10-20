# Aalto-OperatingSystems-Challenge

Repository for the voluntary Challenge Exercise in the Master's course "Operating Systems".

## 0. TODO
- finish the container
- create a dockerfile with the container
- add tutorials for dockerfile
- update installation instructions


## 1. Install docker

As host environment for the docker container Ubuntu 16.04 LTS (64 Bit) was used. To install docker exexcute this on the Ubuntu host machine:
```shell
sudo apt-get update
sudo apt-get install linux-image-extra-$(uname -r) linux-image-extra-virtual
sudo apt-get isntall apt-transport-https ca-certificates curl software-properties-common
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
To verify the installtion run:
```shell
sudo docker run hello-world
```
sources: https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/


## 2. Using the dockerfile

//TODO how to install the dockerfile

The dockerfile executes the following installation for you and delivers a fully functional docker container.

## 3. Manual installation
### a) Using a docker image with tensorflow binaries
#### Execute the following commands on the host system to start a docker container with CPU support only and connect via bash:
```shell
docker run -it -p hostPort:containerPort gcr.io/tensorflow/tensorflow:lates-devel bash
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

### Install the object detection API

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
$export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim
```
#### Verify the installation
```shell
$python object_detection/builders/model_builder_test.py
```
source: https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/installation.md

### 4. Usage

Start the container using:

To edit and run the jupyter notebook navigate to the /tensorflow/models/research/object_detection/ folder and run the notebook server with:
```shell
jupyter notebook --allow-root
```
Or just run the python script in the same folder with:
```shell
//TODO
```

Once started the the container sends the collected metadata (amount of cars, array with their positions in the image, and probability for each car to actually be a car) to a server.

//TODO specify the server as input arg for python script








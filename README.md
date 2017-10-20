# Aalto-OperatingSystems-Challenge

Repository for the voluntary Challenge Exercise in the Master's course "Operating Systems".

## TODO
- finish the container
- create a dockerfile with the container
- add tutorials for dockerfile
- update installation instructions

## Install docker

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


## Using a docker image with tensorflow binaries
### Execute the following commands on the host system to start a docker container with CPU support only and connect via bash:
```shell
docker run -it -p hostPort:containerPort gcr.io/tensorflow/tensorflow:lates-devel bash
```
### GPU support TODO


## Install additional TensorFlow functions and the object detection api in the container

### Install additional libraries in the container using bash access
```shell
sudo apt-get install protobuf-compiler python-pil python-lxml
sudo pip install jupyter
sudo pip install pillow
sudo pip install lxml
sudo pip install matplotlib
```

### Install Protbuf Compiler in the container
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
### Add Libraries to Pythonpath
Run this command in every terminal started or add them to your ~/.bashrc
```shell
$export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim
```
### Verify the installation
```shell
$python object_detection/builders/model_builder_test.py
```
source: https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/installation.md

## FROM HERE ON TODO:
get tensorflow model stuff from









# coding: utf-8

# # Car Detector
# This script is based on the object detection api from https://github.com/tensorflow/models/tree/master/research/object_detection. More instruction on how to install and what is the purpose: https://github.com/Oleffa/Aalto-OperatingSystems-Challenge

# # Imports

# In[9]:


import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile

import urllib as urllib_2
import urllib2

from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image
import time

from utils import label_map_util

from utils import visualization_utils as vis_util

#Setting up the environment

# This is needed to display the images.
get_ipython().magic(u'matplotlib inline')

# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("..")


# # Model preparation 

# ## Variables
# 
# Models are taken from: [detection model zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md).
# 
# Also use self trained models here.

# In[10]:


#Select model
model = 2 # is not recommended (takes very long)

if model == 1:
    MODEL_NAME = 'ssd_mobilenet_v1_coco_11_06_2017'
if model == 2:
    MODEL_NAME = 'ssd_inception_v2_coco_11_06_2017'
if model == 3:
    MODEL_NAME = 'rfcn_resnet101_coco_11_06_2017'
if model == 4:
    MODEL_NAME = 'faster_rcnn_inception_resnet_v2_atrous_coco_11_06_2017'
        
MODEL_FILE = MODEL_NAME + '.tar.gz'
DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')

NUM_CLASSES = 90

# Download and unpack model
opener = urllib.request.URLopener()
opener.retrieve(DOWNLOAD_BASE + MODEL_FILE, MODEL_FILE)
tar_file = tarfile.open(MODEL_FILE)
for file in tar_file.getmembers():
  file_name = os.path.basename(file.name)
  if 'frozen_inference_graph.pb' in file_name:
    tar_file.extract(file, os.getcwd())


# ## Loading the model and label map

# In[11]:


detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')


# ## Loading label map
# Label maps map indices to category names, so that when our convolution network predicts `5`, we know that this corresponds to `airplane`.  Here we use internal utility functions, but anything that returns a dictionary mapping integers to appropriate string labels would be fine

# In[12]:


label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)


# ## Helper code to load a picture inta an array

# In[13]:


def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)


# In[15]:


# Size, in inches, of the output images.
IMAGE_SIZE = (12, 8)
with detection_graph.as_default():
  with tf.Session(graph=detection_graph) as sess:
    # Definite input and output Tensors for detection_graph
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
    # Each box represents a part of the image where a particular object was detected.
    detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
    # Each score represent how level of confidence for each of the objects.
    # Score is shown on the result image, together with the class label.
    detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
    detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')
    while(True):
        # Download picture
        opener.retrieve("http://tpark-cam.cs.aalto.fi/picture.jpg", "/tensorflow/models/research/object_detection/test_images/picture2.jpg")
        image = Image.open('/tensorflow/models/research/object_detection/test_images/picture2.jpg')
        # the array based representation of the image will be used later in order to prepare the
        # result image with boxes and labels on it.
        image_np = load_image_into_numpy_array(image)
        # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
        image_np_expanded = np.expand_dims(image_np, axis=0)
        # Detect things
        (boxes, scores, classes, num) = sess.run(
            [detection_boxes, detection_scores, detection_classes, num_detections],
            feed_dict={image_tensor: image_np_expanded})

        # extract boxes, count and probabilites of cars with a probability > 0.5
        boxes_list = list()
        final_score = np.squeeze(scores)
        probabilities = list()
        count = 0
        for i in range(100):
            if scores is None or final_score[i] > 0.3: #if the probability of eing a car is > 0.5
                if classes[0][i] == 3:
                    count = count + 1 # count the number of detected cars
                    boxes_list.append(boxes[0][i]) # add the box to the list of data to be sent to the handler   
                    probabilities.append(scores[0][i])
        #print(boxes_list)

        # write stuff to the handler
        data = [('count', count), ('boxes', boxes_list), ('probabilities', probabilities)]
        data = urllib_2.urlencode(data)
        req = urllib2.Request('https://g6-os.herokuapp.com/updateMetadata', data)
        req.add_header("metaData", "application/jason")
        page = urllib2.urlopen(req).read()
        #print page

        # Visualization of the results of a detection.
        visualize = False
        if visualize == True:
            vis_util.visualize_boxes_and_labels_on_image_array(
                image_np,
                np.squeeze(boxes),
                np.squeeze(classes).astype(np.int32),
                np.squeeze(scores),
                category_index,
                use_normalized_coordinates=True,
                min_score_thresh=.3,
                line_thickness=3)
            plt.figure(figsize=IMAGE_SIZE)
            plt.imshow(image_np)
        print(count)


# In[ ]:





# In[ ]:





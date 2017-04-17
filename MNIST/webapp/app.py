# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from flask import render_template

import PIL
import base64
import numpy as np
from PIL import Image
from io import BytesIO
from time import sleep

import tensorflow as tf
import tflearn

app = Flask(__name__, static_url_path='/static')


def build_model():
    tf.reset_default_graph()
    net = tflearn.input_data([None, 784])

    net = tflearn.fully_connected(net, 300, activation='ReLU')
    net = tflearn.fully_connected(net, 100, activation='ReLU')

    net = tflearn.fully_connected(net, 10,  activation='softmax')

    net = tflearn.regression(net, optimizer='sgd', learning_rate=0.05, loss='categorical_crossentropy')

    model = tflearn.DNN(net)
    return model

# criação e carregamento do modelo
model = build_model()
model.load('../MNIST.tfl')

@app.route('/', methods=['POST', 'GET'])
def home():
    resp = None
    if request.method == 'POST':
        data = request.form['canvas']
        data = base64.b64decode(data.replace('data:image/png;base64,', ''))
        img = Image.open(BytesIO(data))
        img = fill_background(img)
        img = resize(img, 28)
        X = do_array(img)
        X = X.reshape(784)
        # import pdb; pdb.set_trace()
        try:
            y = model.predict([X])
            resp = get_answer(y)
        except:
            resp = None
    return render_template('teste.html', resposta=resp)


def resize(img, width):
    wpercent = (width / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((width, hsize), PIL.Image.ANTIALIAS)
    return img


def do_array(img):
    temp = img
    temp = temp.convert('1')
    A = np.array(temp)
    new_A = np.empty((A.shape[0], A.shape[1]), None)

    for i in range(len(A)):
        for j in range(len(A[i])):
            if A[i][j] == True:
                new_A[i][j] = 0
            else:
                new_A[i][j] = 1
    return new_A


def fill_background(image):
    image.convert("RGBA")
    pixel_data = image.load()

    if image.mode == "RGBA":
        for y in range(image.size[1]):
            for x in range(image.size[0]):
                if pixel_data[x, y][3] < 255:
                    pixel_data[x, y] = (255, 255, 255, 255)
    return image


def get_answer(y):
    best = max(y[0])
    return y[0].index(best)

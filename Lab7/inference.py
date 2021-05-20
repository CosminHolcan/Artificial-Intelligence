# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 14:20:51 2021

@author: tudor
"""

import random
import math

import numpy as np
import torch
import torch.nn.functional as F
import matplotlib.pyplot as plt

import myModel



# we load the model

filepath = "myNet.pt"
ann = myModel.Net()

ann.load_state_dict(torch.load(filepath))
ann.eval()

# visualise the parameters for the ann (aka weights and biases)
# for name, param in ann.named_parameters():
#     if param.requires_grad:
#         print (name, param.data)
differences = list()
for _ in range(1000):
    x1 = random.random() * 20 - 10
    x2 = random.random() * 20 - 10
    x = torch.tensor([x1, x2])
    predicted = ann(x).tolist()[0]
    expected = math.sin(x1+x2 / math.pi)
    difference = round(abs(predicted-expected),2)
    differences.append(difference)

plt.plot(differences)
plt.show()

print('Average differences = {:.5f}\n'.format(np.average(differences)))


while True:
    x1 = float(input("x1 = "))
    x2 = float(input("x2 = "))
    x = torch.tensor([x1, x2])
    print("Predicted : ",ann(x).tolist()[0])
    print("Expected : ", math.sin(x1+x2 / math.pi), "\n")
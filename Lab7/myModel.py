# -*- coding: utf-8 -*-

import torch
import torch.nn.functional as F
import torch.nn as nn


class Net(torch.nn.Module):
    # the class for the network

    def __init__(self, n_feature = 2, n_hidden_1 = 20, n_hidden_2 = 50, n_hidden_3 = 20, n_output = 1):
        # we have two layers: a hidden one and an output one
        super(Net, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(n_feature, n_hidden_1),
            nn.GELU(),
            nn.Linear(n_hidden_1, n_hidden_2),
            nn.GELU(),
            nn.Linear(n_hidden_2, n_hidden_3),
            nn.GELU(),
            nn.Linear(n_hidden_3, n_output)
        )

    def forward(self, x):
        # a function that implements the forward propagation of the signal
        # observe the refu function applied on the output of the hidden layer
        return self.model(x)

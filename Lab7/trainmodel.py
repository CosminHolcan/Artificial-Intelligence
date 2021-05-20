import math

import torch
import torch.nn.functional as F
import matplotlib.pyplot as plt
import numpy as np

import myModel

x=list()
y=list()
with open("mydataset.txt", "r") as file:
    n = int(file.readline()[:-1])
    for _ in range(n):
        line = file.readline().strip()
        line_elements = line.split(',')
        x.append((float(line_elements[0]), float(line_elements[1])))
        y.append(float(line_elements[2]))

x = torch.tensor(x)
y = torch.unsqueeze(torch.tensor(y), dim=1)


# we set up the lossFunction as the mean square error
lossFunction = torch.nn.MSELoss()

# we create the ANN
ann = myModel.Net()


# we use an optimizer that implements stochastic gradient descent
optimizer_batch = torch.optim.SGD(ann.parameters(), lr=0.001)

# we memorize the losses forsome graphics
loss_list = []

# we set up the environment for training in batches
batch_size = 50
n_batches = int(len(x) / batch_size)

for epoch in range(2500):

    for batch in range(n_batches):
        # we prepare the current batch  -- please observe the slicing for tensors
        batch_X, batch_y = x[batch * batch_size:(batch + 1) * batch_size],\
                           y[batch * batch_size:(batch + 1) * batch_size]

        # we compute the output for this batch
        prediction = ann(batch_X)

        # we compute the loss for this batch
        loss = lossFunction(prediction, batch_y)

        # we set up the gradients for the weights to zero (important in pytorch)
        optimizer_batch.zero_grad()

        # we compute automatically the variation for each weight (and bias) of the network
        loss.backward()

        # we compute the new values for the weights
        optimizer_batch.step()

        # we print the loss for all the dataset for each 10th epoch
    if epoch % 100 == 99:
        # we save it for graphics
        loss_list.append(loss.tolist())
        y_pred = ann(x)
        loss = lossFunction(y_pred, y)
        print('\repoch: {}\tLoss =  {:.5f}'.format(epoch, loss))

    # Specify a path
filepath = "myNet.pt"

# save the model to file
torch.save(ann.state_dict(), filepath)

# visualise the parameters for the ann (aka weights and biases)
# for name, param in ann.named_parameters():
#     if param.requires_grad:
#         print (name, param.data)


plt.plot(loss_list)
plt.show()
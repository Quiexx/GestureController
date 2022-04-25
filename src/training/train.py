import os

import torch
import numpy as np
import random
from torch.utils.data import DataLoader
from torch import nn
import pickle

from src.training.train_utils import GesturesDataset, device, train_loop, test_loop

# Load data
data_dir = "../dataset/data"
gesture_count = 9

X_list = []
y_list = []
for gesture_num in os.listdir(data_dir):
    gest_dir = os.path.join(data_dir, gesture_num)
    for x_f in os.listdir(gest_dir):
        x_path = os.path.join(gest_dir, x_f)
        X_list.append(np.load(x_path))
        y_list.append(np.array(int(gesture_num)))

X = np.array(X_list)
y = np.array(y_list)

N = X.shape[0]
train_part = 3510  # 65%
val_part = 1080  # 20%
test_part = 810  # 15%

rand_indices = list(range(N))
random.shuffle(rand_indices)

train_indices = rand_indices[:train_part]
val_indices = rand_indices[train_part: val_part + train_part]
test_indices = rand_indices[val_part + train_part:]

X_train = X[train_indices]
y_train = y[train_indices]

X_val = X[val_indices]
y_val = y[val_indices]

X_test = X[test_indices]
y_test = y[test_indices]

train_data = GesturesDataset(y_train, X_train, transform=torch.from_numpy)
val_data = GesturesDataset(y_val, X_val, transform=torch.from_numpy)
test_data = GesturesDataset(y_test, X_test, transform=torch.from_numpy)

# 2D
# model = nn.Sequential(
#     nn.BatchNorm1d(42),
#     nn.Linear(42, 9),
#     nn.Softmax(dim=1)
# )

# 3D
# model = nn.Sequential(
#     nn.BatchNorm1d(63),
#     nn.Linear(63, 9),
#     nn.Softmax(dim=1)
# )

# 3D Nonlinear
model = nn.Sequential(
    nn.BatchNorm1d(63),
    nn.Linear(63, 100),
    nn.ReLU(),
    nn.Linear(100, 9),
    nn.Softmax(dim=1)
)

model = model.to(device)

# Training
learning_rate = 5e-1
batch_size = 128
epochs = 300

train_dataloader = DataLoader(train_data, batch_size=batch_size, shuffle=True)
val_dataloader = DataLoader(val_data, batch_size=batch_size, shuffle=True)
test_dataloader = DataLoader(test_data, batch_size=batch_size, shuffle=True)

loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

best_acc = None
best_loss = None
best_acc_epoch = None
best_loss_epoch = None

print("Training:")
for t in range(epochs):
    print(f"Epoch {t + 1}\n-------------------------------")
    train_loop(train_dataloader, model, loss_fn, optimizer)
    acc, loss = test_loop(val_dataloader, model, loss_fn)

    if best_acc is None or acc > best_acc:
        best_acc = acc
        best_acc_epoch = t + 1

    if best_loss is None or loss < best_loss:
        best_loss = acc
        best_loss_epoch = t + 1


print("Test:")
test_loop(test_dataloader, model, loss_fn)
print()
print(f"Best acc: {best_acc * 100}% in epoch {best_acc_epoch}")
print(f"Best loss: {best_loss}% in epoch {best_loss_epoch}")


# Saving
to_save = input("Save?(y/n): ")
if to_save.lower() == "y":
    model.eval()
    model_name = input("Model name: ")
    with open("../app/model/learned_models/" + model_name, "wb") as f:
        pickle.dump(model, f)

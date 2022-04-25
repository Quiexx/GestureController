import torch
import json
import numpy as np
import random
from torch.utils.data import DataLoader
from torch import nn
import pickle

# Load data
from src.training.train_utils import GesturesDataset, device, train_loop, test_loop

with open("../dataset/gesture_ds.json", "r") as f:
    data = json.load(f)

# Data preparation
classes = {cls_num: cls for cls_num, cls in enumerate(data)}

ds_len = sum((len(lst) for lst in data.values()))
data_shape = np.array(list(data.values())[0]).shape
feature_cnt = data_shape[-1]
X = np.ndarray((ds_len, feature_cnt))
y = np.ndarray((X.shape[0],), dtype=int)

x_i = 0
for cls_num, cls in classes.items():
    pos = np.array(data[cls])
    for lst in pos:
        X[x_i] = lst
        y[x_i] = cls_num
        x_i += 1

N = X.shape[0]
train_part = 1755  # 65%
val_part = 540  # 20%
test_part = 405  # 15%

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

model = nn.Sequential(
    nn.BatchNorm1d(42),
    nn.Linear(42, 9),
    nn.Softmax(dim=1)
)

model = model.to(device)

# Training
learning_rate = 5e-2
batch_size = 64
epochs = 140

train_dataloader = DataLoader(train_data, batch_size=batch_size, shuffle=True)
val_dataloader = DataLoader(val_data, batch_size=batch_size, shuffle=True)
test_dataloader = DataLoader(test_data, batch_size=batch_size, shuffle=True)

loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

print("Training:")
for t in range(epochs):
    print(f"Epoch {t + 1}\n-------------------------------")
    train_loop(train_dataloader, model, loss_fn, optimizer)
    test_loop(val_dataloader, model, loss_fn)

print("Test:")
test_loop(test_dataloader, model, loss_fn)

# Saving
to_save = input("Save?(y/n): ")
if to_save.lower() == "y":
    model.eval()
    model_name = input("Model name: ")
    with open("../app/model/learned_models/" + model_name, "wb") as f:
        pickle.dump(model, f)

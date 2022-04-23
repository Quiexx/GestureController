import torch
from torch.utils.data import Dataset

device = "cpu"

class GesturesDataset(Dataset):
    def __init__(self, y, x, transform=None, target_transform=None):
        self.y = y
        self.x = x

        self.transform = transform
        self.target_transform = target_transform

        if self.transform:
            self.x = self.transform(self.x)
        if self.target_transform:
            self.y = self.target_transform(self.y)

    def __len__(self):
        return len(self.y)

    def __getitem__(self, idx):
        track = self.x[idx]
        label = self.y[idx]
        return track, label


def train_loop(dataloader, model, loss_fn, optimizer):
    size = len(dataloader.dataset)
    for batch, (X, y) in enumerate(dataloader):
        X, y = X.to(device).float(), y.to(device).long()

        # Compute prediction and loss
        pred = model(X)
        loss = loss_fn(pred, y)

        # Backpropagation
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if batch % 10 == 0:
            loss, current = loss.item(), batch * len(X)
            print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")


def test_loop(dataloader, model, loss_fn):
    size = len(dataloader.dataset)
    num_batches = len(dataloader)
    test_loss, correct = 0, 0

    with torch.no_grad():
        for X, y in dataloader:
            X, y = X.to(device).float(), y.to(device).long()
            pred = model(X)
            test_loss += loss_fn(pred, y).item()
            correct += (pred.argmax(1) == y).type(torch.float).sum().item()

    test_loss /= num_batches
    correct /= size
    print(f"Test Error: \n Accuracy: {(100 * correct):>0.1f}%, Avg loss: {test_loss:>8f} \n")

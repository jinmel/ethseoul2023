"""Model trainer for pytorch based custom built models."""
import copy
import os

from absl import app
from absl import flags
from absl import logging
import torch
import torch.nn as nn
import torch.optim as optim
import tqdm
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE

from ezkl import export
from models import SimpleModel


FLAGS = flags.FLAGS
flags.DEFINE_string('output_dir', None, 'Output path of exported onnx model.')


def load_data(csv_filename):
    """Load eth fraud dataset from csv."""

    df = pd.read_csv(csv_filename, index_col=0)
    df = df.iloc[:, 2:]
    # Drop object columns
    categories = df.select_dtypes('O').columns.astype('category')
    df.drop(df[categories], axis=1, inplace=True)
    df.fillna(df.median(), inplace=True)

    # Drop columns with variance == 0
    df.drop(df.var()[df.var() == 0].index, axis=1, inplace=True)

    # Drop highly correlated features.
    drop = ['total transactions (including tnx to create contract',
        'total ether sent contracts',
        'max val sent to contract',
        ' ERC20 avg val rec',
        ' ERC20 avg val rec',
        ' ERC20 max val rec',
        ' ERC20 min val rec',
        ' ERC20 uniq rec contract addr',
        'max val sent',
        ' ERC20 avg val sent',
        ' ERC20 min val sent',
        ' ERC20 max val sent',
        ' Total ERC20 tnxs',
        'avg value sent to contract',
        'Unique Sent To Addresses',
        'Unique Received From Addresses',
        'total ether received',
        ' ERC20 uniq sent token name',
        'min value received',
        'min val sent',
        ' ERC20 uniq rec addr']
    # Drop mostly 0
    drop += ['min value sent to contract', ' ERC20 uniq sent addr.1']
    df.drop(drop, axis=1, inplace=True)

    y = df.iloc[:, 0]
    X = df.iloc[:, 1:]
    return X.to_numpy(), y.to_numpy()


def train(model, X_train, y_train, X_val, y_val):
    # loss function and optimizer
    X_train = torch.from_numpy(X_train).type(torch.float32)
    # y_train = F.one_hot(torch.from_numpy(y_train)).type(torch.float32)
    y_train = torch.from_numpy(y_train).type(torch.float32).reshape(-1, 1)
    X_val = torch.from_numpy(X_val).type(torch.float32)
    # y_val = F.one_hot(torch.from_numpy(y_val)).type(torch.float32)
    y_val = torch.from_numpy(y_val).type(torch.float32).reshape(-1, 1)

    loss_fn = nn.BCELoss()  # binary cross entropy
    optimizer = optim.Adam(model.parameters(), lr=0.0005)

    n_epochs = 50   # number of epochs to run
    batch_size = 1024  # size of each batch
    batch_start = torch.arange(0, len(X_train), batch_size)

    # Hold the best model
    best_acc = -np.inf   # init to negative infinity
    best_weights = None

    for epoch in range(n_epochs):
        model.train()
        with tqdm.tqdm(batch_start, unit="batch", mininterval=0) as bar:
            bar.set_description(f"Epoch {epoch}")
            for start in bar:
                # take a batch
                X_batch = X_train[start:start+batch_size]
                y_batch = y_train[start:start+batch_size]
                # forward pass
                y_pred = model(X_batch)
                loss = loss_fn(y_pred, y_batch)
                # backward pass
                optimizer.zero_grad()
                loss.backward()
                # update weights
                optimizer.step()
                # print progress
                acc = (y_pred.round() == y_batch).float().mean()
                bar.set_postfix(
                    loss=float(loss),
                )
        # evaluate accuracy at end of each epoch
        model.eval()
        y_pred = model(X_val)
        acc = (y_pred.round() == y_val).float().mean()
        acc = float(acc)
        if acc > best_acc:
            best_acc = acc
            best_weights = copy.deepcopy(model.state_dict())
    # restore model and return best accuracy
    model.load_state_dict(best_weights)
    return best_acc


def main(_):
    X, y = load_data('./transaction_dataset.csv')
    X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2)
    oversample = SMOTE()
    X_train_resample, y_train_resample = oversample.fit_resample(
            X_train, y_train)
    model = SimpleModel()
    best_acc = train(model, X_train_resample, y_train_resample, X_test, y_test)
    print(f'best_model acc: {best_acc}')
    logging.info('Writing onnx file to %s', FLAGS.output_dir)
    export(model, input_shape=[16],
           onnx_filename=os.path.join(FLAGS.output_dir, 'model.onnx'),
           input_filename=os.path.join(FLAGS.output_dir, 'input.json'))
    torch.save(model.state_dict(), os.path.join(FLAGS.output_dir, 'model.pt'))


if __name__ == '__main__':
    app.run(main)

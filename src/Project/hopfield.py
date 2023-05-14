# Loading data

import numpy as np
import matplotlib.pyplot as plt
import torch
import torchvision

from torchvision import transforms
from copy import deepcopy

def load_mnist(batch_size,norm_factor=1):
    transform = transforms.Compose([transforms.ToTensor()])
    trainset = torchvision.datasets.MNIST(root='./mnist_data', train=True,
                                            download=True, transform=transform)
    print("trainset: ", trainset)
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size,
                                            shuffle=True)
    print("trainloader: ", trainloader)
    trainset = list(iter(trainloader))

    testset = torchvision.datasets.MNIST(root='./mnist_data', train=False,
                                        download=True, transform=transform)
    testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size,
                                            shuffle=True)
    testset = list(iter(testloader))
    for i,(img, label) in enumerate(trainset):
        trainset[i] = (img.reshape(len(img),784) /norm_factor ,label)
    for i,(img, label) in enumerate(testset):
        testset[i] = (img.reshape(len(img),784) /norm_factor ,label)
    return trainset, testset


def demircigil_update_rule(z, xs):
    out = torch.zeros(len(z), 1)
    # loop over every element of z
    for i in range(len(z)):
        # initialize accumulators for E_positive and E_negative
        E_pos = 0
        E_neg = 0
        # make copies so we don't mutate the original array
        z_pos = deepcopy(z)
        z_neg = deepcopy(z)
        # try both z[l]^+ and z[l]^-
        z_pos[i] = 1
        z_neg[i] = -1
        # for each stored pattern in xs
        for x in xs:
            # compute positive or negative energies
            E_plus = x.T @ z_pos
            E_minus = x.T @ z_neg
            # accumulate their exponents
            E_pos += torch.exp(E_plus / 10)
            E_neg += torch.exp(E_minus / 10)
        # if energy is greater flip
        if E_pos > E_neg:
            out[i] = 1
        else:
            out[i] = -1
    return out


def binarize(img):
    """
    since the discrete hopfield network's neurons have only two states -1,1,
     therefore we should binarize mnist digits
    """
    i = deepcopy(img)
    i[img > 0] = -1
    i[img <=0] = 1
    return i

def zero_bottom_half(img):
    i = deepcopy(img)
    H, W = img.shape
    i[H // 2:H, :] = -1
    return i

def addnoise(train, error_rate=0.15):
    """
    Adds random noise to the train data and returns it as the test data.
    Noise is added by flipping the sign of some units with the error rate p.

    """
    print(train)
    test = np.copy(train) # cf. from copy import copy/deepcopy
    for i, t in enumerate(test):
        s = np.random.binomial(1, error_rate, len(t))
        for j in range(len(t)):
            if s[j] != 0:
                t[j] *= -1
    return test

def is_retrived(input, out):
    """
    returns true if the output is equal to the input
    """
    return np.array_equal(input, out)


def is_in_the_memory(memory, out):
    """
    returns true if the output is a retrived pattern from the memory of the network
    """
    for input in memory:
        if is_retrived(input, out):
            return True
    return False


def is_well_classified(out, patterns, test_label, train_labels):
    """
    returns true if the digit is well classified,
    arguments are :
    out : the output returned by the model's prediction
    patterns : the model's memorized patterns
    train_labels : the labels of training set
    test_labels : the labels of test set
    """
    for i in range(len(patterns)):
        if is_retrived(patterns[i], out):
            if train_labels[i] == test_label:
                return (True, test_label)
            else:
                return (False, train_labels[i])
    return (False, -1)


# defining the hopfield class
class DiscreteHopfieldNetwork():
    def __init__(self, nsp, x_train, y_train):
        self.nb_neurons = 784
        self.nb_storedPatterns = nsp
        self.storedPatterns = [binarize(x_train[i, :].reshape(784, 1)) for i in range(nsp)]
        self.storedLabels = [y_train[i] for i in range(nsp)]
        self.W = torch.zeros((784, 784))

    def retrieve_store_demircigil(self, break_val=-1, plot=True):
        N = self.nb_storedPatterns
        xs = self.storedPatterns
        for j in range(N):
            # so we don't print a huge number of images for large stored patterns
            if break_val > 0:
                if j > break_val:
                    break
            halved_digit = addnoise(xs[j], 0.15).reshape(784, 1)
            out = demircigil_update_rule(halved_digit, xs)
            if plot:
                fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(12, 4))
                imgs = [xs[j], halved_digit, out]
                titles = ["Original", "Masked", "Reconstruction"]
                for i, ax in enumerate(axs.flatten()):
                    plt.sca(ax)
                    plt.imshow(imgs[i].reshape(28, 28))
                    plt.title(titles[i])
                plt.show()

    def unnoise(self, input, plot=True):
        input = binarize(input).reshape(784, 1)
        # the input is a img of shape (784, 1)
        xs = self.storedPatterns
        corrupted_digit = addnoise(input, 0.15).reshape(784, 1)
        out = demircigil_update_rule(corrupted_digit, xs)
        if plot:
            fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(12, 4))
            imgs = [input, corrupted_digit, out]
            titles = ["Original", "Corrupted", "Reconstruction"]
            for i, ax in enumerate(axs.flatten()):
                plt.sca(ax)
                plt.imshow(imgs[i].reshape(28, 28))
                plt.title(titles[i])
            plt.show()
        return out

    def classify(self, input, plot=True):
        if plot:
            plt.imshow(binarize(input.reshape(28, 28)))
        xs = self.storedPatterns
        out = demircigil_update_rule(binarize(input.reshape(784, 1)), xs)
        for i in range(len(xs)):
            if is_retrived(xs[i], out):
                return int(self.storedLabels[i])
        return -1

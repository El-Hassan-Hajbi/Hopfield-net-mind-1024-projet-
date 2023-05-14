import json

import joblib as joblib
import torch
from django.http import JsonResponse
from django.shortcuts import render

from .hopfield import load_mnist, DiscreteHopfieldNetwork, addnoise


def main_page(request):
    return render(request, "index.html")

def run_model_view(request):
    result = 1
    return JsonResponse({'result': result})


def classify_view(request):
    if request.method == 'POST':
        try:
            payload = json.loads(request.body)
            input_data = torch.tensor(payload.get('input'), dtype=torch.float32)
            xtrain_data = torch.tensor(payload.get('xtrain'), dtype=torch.float32)
            ytrain_data = torch.tensor(payload.get('ytrain'))

            # Process the input_data, xtrain_data, and ytrain_data as needed

            # Your classification logic using the input, xtrain, and ytrain data

            model = joblib.load("Completed_model.joblib")
            classification = model.classify(input_data, plot=False)

            return JsonResponse({'result': classification})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON payload'})
    else:
        return JsonResponse({'error': 'Invalid request method'})
def load_data_view(request):
    trainset, testset = load_mnist(100)

    x_train, y_train = trainset[0]
    x_test, y_test = testset[0]
    #x_test, y_test = x_test[0:200, ], y_test[0:200]
    model = DiscreteHopfieldNetwork(10, x_train, y_train)
    joblib.dump(model, "Completed_model.joblib")
    return JsonResponse({'Xtrain' :x_train.numpy().tolist(),'Ytrain' :y_train.numpy().tolist(),'Xtest' :x_test.numpy().tolist(),'Ytest' :y_test.numpy().tolist() })

def noise_view(request):
    if request.method == 'POST':
        try:
            payload = json.loads(request.body)
            input_data = torch.tensor(payload.get('input'), dtype=torch.float32).view(-1, 1)
            res = addnoise(input_data)
            return JsonResponse({'result': res.squeeze().tolist()})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON payload'})
    else:
        return JsonResponse({'error': 'Invalid request method'})

def unnoise_view(request):
    if request.method == 'POST':
        try:
            payload = json.loads(request.body)
            input_data = torch.tensor(payload.get('input'), dtype=torch.float32).view(-1, 1)
            model = joblib.load("Completed_model.joblib")
            res = model.unnoise(input_data, plot=False)
            return JsonResponse({'result': res.squeeze().tolist()})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON payload'})
    else:
        return JsonResponse({'error': 'Invalid request method'})
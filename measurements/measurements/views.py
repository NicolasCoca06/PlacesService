from .models import Measurement
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse
from django.urls import reverse
from django.conf import settings
import requests
import json

def check_variable(data):
    r = requests.get(settings.PATH_VAR, headers={"Accept":"application/json"})
    variables = r.json()
    for variable in variables:
        if data["variable"] == variable["id"]:
            return True
    return False

def check_place(data):
    r = requests.get(settings.PATH_PLACE, headers={"Accept":"application/json"})
    places = r.json()
    for place in places:
        if data["place"] == place["name"]:
            return True
    return False

def obtain_id_place(name_place):
    r = requests.get(settings.PATH_PLACE, headers={"Accept":"application/json"})
    places = r.json()
    for place in places:
        if name_place == place["name"]:
            return place["id"]
    return None

def MeasurementList(request):
    queryset = Measurement.objects.all()
    context = list(queryset.values('id', 'variable', 'value', 'unit', 'place', 'dateTime'))
    return JsonResponse(context, safe=False)

def MeasurementCreate(request):
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        data_json = json.loads(data)
        if check_variable(data_json) == True:
            if check_place(data_json) == True:
                measurement = Measurement()
                measurement.variable = data_json['variable']
                measurement.value = data_json['value']
                measurement.unit = data_json['unit']
                id_place = obtain_id_place(data_json['place'])
                measurement.place = int(id_place)
                measurement.save()
                return HttpResponse("successfully created measurement")
            else:
                return HttpResponse("unsuccessfully created measurement. Place does not exist")
        else:
            return HttpResponse("unsuccessfully created measurement. Variable does not exist")

def MeasurementsCreate(request):
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        data_json = json.loads(data)
        measurement_list = []
        for measurement in data_json:
            if check_variable(measurement) == True:
                if check_place(measurement) == True:
                    db_measurement = Measurement()
                    db_measurement.variable = measurement['variable']
                    db_measurement.value = measurement['value']
                    db_measurement.unit = measurement['unit']
                    id_place = obtain_id_place(measurement['place'])
                    db_measurement.place = int(id_place)
                    measurement_list.append(db_measurement)
                else:
                    return HttpResponse("unsuccessfully created measurement. Place does not exist")
            else:
                return HttpResponse("unsuccessfully created measurement. Variable does not exist")
        
        Measurement.objects.bulk_create(measurement_list)
        return HttpResponse("successfully created measurements")
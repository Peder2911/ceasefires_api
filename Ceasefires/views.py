from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import pandas as pd
from io import BytesIO
import json

import logging

from django.conf import settings

from django.db import transaction

import requests

from Ceasefires.util import replaceData

@transaction.atomic
def updateData(request):
    if request.method == "GET":
        tmpl = loader.get_template("update.html")
        return HttpResponse(tmpl.render(request=request))

    elif request.method == "POST":

        data = {}

        try:
            b = BytesIO(request.FILES["dataset"].read())
            b.seek(0)
            #data["declarations"] = pd.read_excel(b)
            b.seek(0)
        except KeyError:
            return HttpResponse("Something went wrong",status_code=500)

        r = requests.post(settings.RELATIONIZER_URL,
            files = {"dataset.xlsx": b}) 
        if r.status_code != 200:
            raise ValueError("Api gave 500!!")
        response = r.json()
        if response["ok"]:
            data.update({key:pd.DataFrame(dat) for key,dat in response["data"].items()})
        else:
            return HttpResponse("There is something wrong with the data!",status=400)

        replaceData(data)
        return HttpResponse("Success")

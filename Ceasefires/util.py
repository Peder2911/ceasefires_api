
from Ceasefires.models import *
import pandas as pd
from datetime import datetime

from typing import Dict

import re

import logging

def replaceData(data: Dict[str,pd.DataFrame]):

    for m in [Region,Country,Ceasefire,Actor,Declaration]:
        m.objects.all().delete()

    try:
        R = Region.objects.get(code = -1)
    except Region.DoesNotExist:
        R = Region.objects.create(
            code = -1,
            name = "dud"
            )

    for idx,row in data["countries"].iterrows():
        Country.objects.create(
            code = row.cc,
            region = R,
            name = row.location
        )

    for idx,row in data["ceasefires"].iterrows():
        year = row.cf_effect_yr if not row.cf_effect_yr in [-1,0] else None 
        month = row.cf_effect_month if not row.cf_effect_month in [-1,0] else 6
        day = row.cf_effect_day if not row.cf_effect_day in [-1,0] else 15 
        
        try:
            d = datetime.strptime(f"{year}-{month}-{day}",
                "%Y-%m-%d")
        except ValueError:
            d = None

        ctry = Country.objects.get(code=row.cc)
        cf = Ceasefire.objects.create(
            code = row.uniq_id,
            country = ctry,
            effect_date = d,
        )

    for idx,row in data["actors"].iterrows():
        Actor.objects.create(
            code = row.acid,
            ucdp_code = row.ucdp_actor_id,
            name = row.actor_name
        )

    for idx,row in data["declarations"].iterrows():
        #row["acid"] = row["actor_name"] + "@" + str(row["cc"])

        default = lambda x: x if x not in [-1,0] else None
        year,month,day = [default(v) for v in [row.cf_dec_yr, row.cf_dec_month, row.cf_dec_day]]

        month = month if month else 6
        day = day if day else 15

        try:
            date = datetime.strptime(f"{year}-{month}-{day}",
                "%Y-%m-%d")
        except ValueError:
            continue
        else:
            Declaration.objects.create(
                ceasefire = Ceasefire.objects.get(code=row.uniq_id),
                #country = Country.objects.get(code=row.cc),
                actor = Actor.objects.get(code=row.acid),
                dec_date = date
            )

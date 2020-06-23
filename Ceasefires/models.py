
from django.db import models

class Region(models.Model):
    code = models.IntegerField(primary_key=True)
    name= models.CharField(max_length=255)
    def __str__(self):
        return f"{self.name}"

class Country(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length = 255)
    region = models.ForeignKey(Region,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"

class Ceasefire(models.Model):
    code = models.CharField(max_length=128,primary_key=True)
    effect_date = models.DateField(null=True)
    country = models.ForeignKey(Country,on_delete=models.CASCADE)

    def __str__(self):
        return f"A ceasefire @ {self.effect_date} in {self.country}"

class Actor(models.Model):
    code = models.CharField(max_length=128,primary_key=True)
    ucdp_code = models.IntegerField()
    name = models.CharField(max_length = 255)
    def __str__(self):
        return self.code

class Declaration(models.Model):

    ceasefire = models.ForeignKey(Ceasefire, on_delete=models.CASCADE)
    actor = models.ForeignKey(Actor,related_name="ActorA",on_delete=models.CASCADE)

    dec_date = models.DateField()

    def __str__(self):
        return f"{self.actor.name} in {self.ceasefire.country.name} @ {self.dec_date}"


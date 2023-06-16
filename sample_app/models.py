from django.db import models

class Banner(models.Model):
    banner_id = models.CharField(max_length=200, blank=True, default='')
    name = models.CharField(max_length=200, blank=True, default='')
    wiki_link = models.CharField(max_length=200, blank=True, default='')
    start_date = models.CharField(max_length=200, blank=True, default='') # Temporary, change to DateField
    #start_date = models.DateField(blank=True, null=True)
    end_date = models.CharField(max_length=200, blank=True, default='') # Temporary, change to DateField
    #end_date = models.DateField(blank=True, null=True)
    region = models.CharField(max_length=200, blank=True, default='')
    jp_banner = models.OneToOneField('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='en_banner')

    def __str__(self):
        return self.name
        

class Servant(models.Model):
    servant_id = models.IntegerField(primary_key=True)
    status = models.CharField(max_length=200, blank=True, default='')
    name = models.CharField(max_length=200, blank=True, default='')
    rateups = models.ManyToManyField(Banner)

    def __str__(self):
        return self.name

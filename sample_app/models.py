from django.db import models

class Banner(models.Model):
    jp_name = models.CharField(max_length=200, blank=True, default='')
    en_name = models.CharField(max_length=200, blank=True, default='')
    jp_wiki_link = models.CharField(max_length=200, blank=True, default='')
    en_wiki_link = models.CharField(max_length=200, blank=True, default='')
    jp_start_date = models.DateField(blank=True, null=True)
    en_start_date = models.DateField(blank=True, null=True)
    jp_end_date = models.DateField(blank=True, null=True)
    en_end_date = models.DateField(blank=True, null=True)
    jp_banner_id = models.CharField(max_length=200, blank=True, default='')
    en_banner_id = models.CharField(max_length=200, blank=True, default='')

    def __str__(self):
        return self.en_name if (self.en_name != '' and self.en_name != None) else self.jp_name
        

class Servant(models.Model):
    servant_id = models.IntegerField(primary_key=True)
    status = models.CharField(max_length=200, blank=True, default='')
    name = models.CharField(max_length=200, blank=True, default='')
    rateups = models.ManyToManyField(Banner)
    pass

    def __str__(self):
        return self.name

from django.contrib import admin

from .models import Banner, Servant
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from import_export.widgets import ManyToManyWidget

class ServantResource(resources.ModelResource):
    rateups = fields.Field(
        column_name='rateups',
        attribute='rateups',
        # Separator for JSON list
        widget=ManyToManyWidget(Banner, field='banner_id')
    )
    class Meta:
        model = Servant
        skip_unchanged = True
        report_skipped = False
        import_id_fields = ('servant_id',)

class ServantAdmin(ImportExportModelAdmin):
    resource_classes = [ServantResource]
    

admin.site.register(Banner)
admin.site.register(Servant, ServantAdmin)

from django.contrib import admin

from .models import Banner, Servant
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from import_export.widgets import ManyToManyWidget, ForeignKeyWidget
from django.core.exceptions import ObjectDoesNotExist

class ServantResource(resources.ModelResource):
    rateups = fields.Field(
        column_name='rateups',
        attribute='rateups',
        widget=ManyToManyWidget(Banner, field='banner_id')
    )
    class Meta:
        model = Servant
        skip_unchanged = True
        report_skipped = False
        import_id_fields = ('servant_id',)

class BannerResource(resources.ModelResource):
    jp_banner = fields.Field(
        column_name='jp_banner',
        attribute='jp_banner',
        widget=ForeignKeyWidget(Banner, field='banner_id')
    )
    class Meta:
        model = Banner
        skip_unchanged = True
        report_skipped = False
        import_id_fields = ('banner_id',)

class ServantAdmin(ImportExportModelAdmin):
    resource_classes = [ServantResource]

class BannerAdmin(ImportExportModelAdmin):
    resource_classes = [BannerResource]

admin.site.register(Banner, BannerAdmin)
admin.site.register(Servant, ServantAdmin)

from django.views import View
from inertia import render
import logging
from .models import Servant, Banner

class Index(View):
    def get(self, request):
        logger = logging.getLogger("Index")
        logger.debug("DEBUG")
        logger.info("INFO")
        logger.error("ERROR")
        logger.warning("WARNING")
        logger.critical("CRITICAL HIT! ")
        banners = Banner.objects.all()
        banner_names = [str(banner) for banner in banners]
        return render(request, 'sample_app/index', props={
            'events': banner_names,
            'page_name': 'Home'
        })


class About(View):
    def get(self, request):
        servants = Servant.objects.all()
        servant_ids = [servant.servant_id for servant in servants]
        return render(request, 'sample_app/about', props={
            'events': servant_ids,
            'page_name': 'About us'
        })

class Event(View):
    def get(self, request, servant_id):
        servant = Servant.objects.get(pk=servant_id)
        return render(request, 'sample_app/event', props={
            'servant_id': servant.servant_id,
            'status': servant.status,
            'name': servant.name
        })

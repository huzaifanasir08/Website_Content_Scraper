from django.contrib import admin
from .bg_tasks import run_scraping

# Customizing the admin interface
class ScrapingStatusAdmin(admin.ModelAdmin):
    actions = [
        'trigger_run_scraping',
    ]
    def trigger_run_scraping(self, request, queryset):
        run_scraping.delay()
        self.message_user(request, "Scraping Task has been triggered.")

    trigger_run_scraping.short_description = "Trigger 'Scraping Task' Task"



# Register the ScrapingStatus model with the custom admin class
admin.site.register(ScrapingStatus, ScrapingStatusAdmin)




from django.contrib import admin
from .models import ScrapingStatus
from .bg_tasks import run_scraping

# Customizing the admin interface
class ScrapingStatusAdmin(admin.ModelAdmin):
    list_display = ('remaining_webs', 'last_web_name', 'last_web_url', 'fetching_started_on', 'internal_links', 'chunk_details', 'successful_fetching', 'fetching_completed_on', 'details')
    search_fields = ('last_web_name', 'last_web_url')
    list_filter = ('successful_fetching',)
    actions = [
        'trigger_run_scraping',
    ]
    def trigger_run_scraping(self, request, queryset):
        run_scraping.delay()
        self.message_user(request, "Scraping Task has been triggered.")

    trigger_run_scraping.short_description = "Trigger 'Scraping Task' Task"



# Register the ScrapingStatus model with the custom admin class
admin.site.register(ScrapingStatus, ScrapingStatusAdmin)




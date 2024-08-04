from django.contrib import admin
from io import StringIO
from django.core.management import call_command
from .models import Category, Item, Review, Marketplace, ItemMarketplace

# Действие для запуска автоматизации
def run_automatization_process(modeladmin, request, queryset):
    out = StringIO()
    call_command('automatization_process', stdout=out)
    result_message = out.getvalue()
    out.close()
    modeladmin.message_user(request, result_message)

run_automatization_process.short_description = "Run automatization process"

def fetch_products(self, request, queryset):
    out = StringIO()
    call_command('fetch_and_save_products', stdout=out)
    result_message = out.getvalue()
    out.close()
    self.message_user(request, "Started fetching products...")
    self.message_user(request, result_message, level='INFO' if "successfully" in result_message.lower() else 'ERROR')
    self.message_user(request, "Finished fetching products.")

fetch_products.short_description = "Fetch products from API"

def make_active(self, request, queryset):
    queryset.update(is_active=True)
    self.message_user(request, "Selected marketplaces have been activated.")

make_active.short_description = "Activate selected marketplaces"

def make_inactive(self, request, queryset):
    queryset.update(is_active=False)
    self.message_user(request, "Selected marketplaces have been deactivated.")

make_inactive.short_description = "Deactivate selected marketplaces"

def update_average_ratings(modeladmin, request, queryset):
    for item in queryset:
        item.update_average_rating()
        item.save()
    modeladmin.message_user(request, "Average ratings updated successfully")

update_average_ratings.short_description = "Update average ratings"

def create_recommendations(modeladmin, request, queryset):
    for marketplace in queryset:
        out = StringIO()
        call_command('create_recommendations', marketplace_name=marketplace.name, stdout=out)
        result_message = out.getvalue()
        out.close()
        modeladmin.message_user(request, result_message)

create_recommendations.short_description = "Create and update recommendations"

class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'average_rating', 'is_sold', 'created_by']
    list_editable = ['average_rating', 'category']
    search_fields = ['name', 'description']
    list_filter = ['is_sold', 'category', 'created_by', 'average_rating']
    readonly_fields = ['created_at']
    actions = [run_automatization_process, update_average_ratings]

class MarketplaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'is_active']
    list_editable = ['is_active']
    search_fields = ['name']
    actions = [make_active, make_inactive, fetch_products, create_recommendations]

class ItemMarketplaceAdmin(admin.ModelAdmin):
    list_display = ['item', 'marketplace', 'marketplace_rating', 'price']
    list_editable = ['marketplace_rating']
    list_filter = ['marketplace']
    search_fields = ['item__name', 'marketplace__name']

def analyze_sentiments(modeladmin, request, queryset):
    for category in queryset:
        out = StringIO()
        call_command('analyze_setiment_category', json_file_path=".json", category=category.name, stdout=out)
        result_message = out.getvalue()
        out.close()
        modeladmin.message_user(request, f"Sentiment analysis completed for {category.name}: {result_message}", level='INFO')

analyze_sentiments.short_description = "Analyze sentiments for selected categories"

admin.site.register(Category)
admin.site.register(Item, ItemAdmin)
admin.site.register(Review)
admin.site.register(Marketplace, MarketplaceAdmin)
admin.site.register(ItemMarketplace, ItemMarketplaceAdmin)

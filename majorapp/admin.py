from django.contrib import admin
from majorapp.models import Contact_Us,Category,register_table,add_property

class Contact_UsAdmin(admin.ModelAdmin):
    list_display = ["id","name","email","contact_number","email","message"]
    search_fields = ["name","email"]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id","cat_name","description"]
admin.site.register(Contact_Us,Contact_UsAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(register_table)
admin.site.register(add_property)
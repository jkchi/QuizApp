from django.contrib import admin

from .models import Question,Option
# Register your models here.
# admin.site.register(Question)
# admin.site.register(Option)


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('text','question','is_answer') 
    list_filter = ['question']

class OptionInlineAdmin(admin.TabularInline):
    model = Option
    # this parameter control the number of empty field in admin site
    extra = 0
    
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text','quiz') 
    list_filter = ['quiz']
    inlines = [OptionInlineAdmin]
    # this parameter control the number of empty field in admin site
    extra = 0

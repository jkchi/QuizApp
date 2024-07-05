from django.contrib import admin
from nested_admin import NestedTabularInline, NestedModelAdmin
from .models import Quiz
from questions.models import Question,Option

class OptionInlineAdmin(NestedTabularInline):
    model = Option
    extra = 0

class QuestionInlineAdmin(NestedTabularInline):
    model = Question
    inlines = [OptionInlineAdmin]
    extra = 0

@admin.register(Quiz)
class QuizAdmin(NestedModelAdmin):
    inlines = [QuestionInlineAdmin]

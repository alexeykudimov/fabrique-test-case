from django.contrib import admin
from .models import Poll, Question, QuestionAnswer, UserAnswer, CompletedPoll


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description",)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "type", "poll",)


@admin.register(QuestionAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ("id", "question", "answer",)


@admin.register(CompletedPoll)
class CompletedPollsAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "poll", "date",)


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ("id", "completed_poll", "question", "choice", "text_answer",)
from django.db import models


class Poll(models.Model):
    # Модель опроса
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

    def __str__(self):
        return f"Poll: {self.name}"


class Question(models.Model):
    # Модель вопроса
    TYPE = (
        ('text', 'text'),
        ('one ans', 'one ans'),
        ('multi ans', 'multi ans')
    )

    text = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=TYPE, default='text')
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return f"Question: {self.text}"


class QuestionAnswer(models.Model):
    # Модель ответов к вопросу
    answer = models.CharField(max_length=100)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')


class CompletedPoll(models.Model):
    # Модель пройденных опросов
    user_id = models.PositiveIntegerField()
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)


class UserAnswer(models.Model):
    # Модель ответов пользователя
    completed_poll = models.ForeignKey(CompletedPoll, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(QuestionAnswer, on_delete=models.CASCADE, blank=True, null=True)
    text_answer = models.CharField(max_length=100, blank=True, null=True)



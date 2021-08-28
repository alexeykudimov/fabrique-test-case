from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from datetime import datetime
from .models import Poll, Question, CompletedPoll
from .serializers import PollSerializer, QuestionSerializer, PassPollSerializer
from .permissions import IsSuperUser


def get_client_ip(request):
    # Получение IP клиента
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_unique_anonymous_id(ip):
    # Преобразование IP клиента в целочисленный ID пользователя
    return int(''.join(ip.split('.')))


class GetActivePollsListView(ModelViewSet):
    # Получение списка активных опросов
    serializer_class = PollSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Poll.objects.filter(end_date__gte=datetime.now())


class PollViewSet(ModelViewSet):
    # CREATE, UPDATE, DELETE опросов
    serializer_class = PollSerializer
    permission_classes = [IsSuperUser]

    def get_queryset(self):
        return Poll.objects.all()


class QuestionViewSet(ModelViewSet):
    # CREATE, UPDATE, DELETE вопросов
    serializer_class = QuestionSerializer
    permission_classes = [IsSuperUser]

    def get_queryset(self):
        return Question.objects.all()


class UserPollsViewSet(ModelViewSet):
    # Получение списка ответов пользователя
    serializer_class = PassPollSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return CompletedPoll.objects.filter(user_id=self.kwargs['pk']).prefetch_related('answers')


class PassPollViewSet(ModelViewSet):
    # Прохождение опроса
    serializer_class = PassPollSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return CompletedPoll.objects.all()

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            return serializer.save(user_id=self.request.user.id)
        else:
            return serializer.save(
                user_id=get_unique_anonymous_id(get_client_ip(self.request))
            )
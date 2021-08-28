from rest_framework import serializers
from .models import Poll, Question, QuestionAnswer, UserAnswer, CompletedPoll
from .fields import ObjectIDField


class ChoiceSerializer(serializers.ModelSerializer):
    # Сериализатор вариантов ответа

    class Meta:
        model = QuestionAnswer
        fields = ('id', 'answer')
        read_only_fields = ('id', )


class QuestionSerializer(serializers.ModelSerializer):
    # Сериализатор вопроса

    type = serializers.ChoiceField(
        choices=Question.TYPE, default='text'
    )
    choices = ChoiceSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = ("id", "poll", "text", "type", "choices")
        read_only_fields = ('id',)
        extra_kwargs = {
            'poll': {'write_only': True}
        }

    def create_choices(self, question, choices):
        QuestionAnswer.objects.bulk_create(
            [QuestionAnswer(question=question, **d) for d in choices]
        )

    def create(self, validated_data):
        choices = validated_data.pop('choices', [])
        question = Question.objects.create(**validated_data)
        self.create_choices(question, choices)
        return question

    def update(self, instance, validated_data):
        choices = validated_data.pop('choices', [])
        instance.answers.all().delete()
        self.create_choices(instance, choices)
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance


class PollSerializer(serializers.ModelSerializer):
    # Сериализатор опроса

    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = ("id", "name", "description", "start_date", "end_date", "questions")
        read_only_fields = ('id',)


class AnswerSerializer(serializers.ModelSerializer):
    # Сериализатор ответа на вопрос

    choice = ChoiceSerializer(read_only=True)
    choice_id = ObjectIDField(
        queryset=QuestionAnswer.objects.all(),
        write_only=True,
        required=False
    )
    text_answer = serializers.CharField(required=False)


    question = QuestionSerializer(read_only=True)
    question_id = ObjectIDField(
        queryset=Question.objects.all(),
        write_only=True
    )

    class Meta:
        model = UserAnswer
        fields = ('id', 'question_id', 'question', 'choice_id', 'choice', 'text_answer')
        read_only_fields = ('id', )


class PassPollSerializer(serializers.ModelSerializer):
    # Сериализатор прохождения теста/получения тестов по пользователю

    answers = AnswerSerializer(many=True)
    poll = PollSerializer(read_only=True)
    poll_id = ObjectIDField(
        queryset=Poll.objects.all(),
        write_only=True
    )

    class Meta:
        model = CompletedPoll
        fields = ('id', 'user_id', 'poll_id', 'poll', 'date', 'answers')
        read_only_fields = ('id', 'user_id', 'date')

    def create(self, validated_data):
        answers = validated_data.pop('answers', [])
        instance = CompletedPoll.objects.create(**validated_data)
        UserAnswer.objects.bulk_create(
            [UserAnswer(completed_poll=instance, **a) for a in answers]
        )
        return instance
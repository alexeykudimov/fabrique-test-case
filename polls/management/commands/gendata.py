from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ...models import Poll, Question, QuestionAnswer
from datetime import datetime, timedelta


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.create_polls()

    def create_polls(self):
        POLLS = [
            {
                'name': 'About you',
                'description': 'Simple test',
                'questions': [
                    {
                        'text': 'Your name?',
                        'type': 'text',
                    },
                    {
                        'text': 'Your age range?',
                        'type': 'one ans',
                        'answers': [
                            '18-30', '30-45', '45+'
                        ]
                    },
                    {
                        'text': 'Your city?',
                        'type': 'text',
                    }
                ]
            },
            {
                'name': 'About you as a developer',
                'description': 'Simple test',
                'questions': [
                    {
                        'text': 'Your developer level?',
                        'type': 'one ans',
                        'answers': [
                            'Junior', 'Middle', 'Senior'
                        ]
                    },
                    {
                        'text': 'Your developer role?',
                        'type': 'one ans',
                        'answers': [
                            'Frontend', 'Backend', 'Fullstack'
                        ]
                    },
                    {
                        'text': 'Your technology stack?',
                        'type': 'text',
                    }
                ]
            }
        ]


        if Poll.objects.count() == 0:
            for poll in POLLS:
                poll_object = Poll.objects.create(
                    name=poll['name'],
                    description=poll['description'],
                    end_date=datetime.now() + timedelta(days=7)
                )

                for question in poll['questions']:
                    question_object = Question.objects.create(
                        text=question['text'],
                        type=question['type'],
                        poll=poll_object
                    )
                    if 'answers' in question:
                        for answer in question['answers']:
                            QuestionAnswer.objects.create(answer=answer, question=question_object)




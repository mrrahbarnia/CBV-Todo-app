from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from faker import Faker
import random

from ...models import Todo

complete_choices = [
    "complete",
    "pending"
]


class Command(BaseCommand):
    help = "Inserting todos with random status"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()

    def handle(self, *args, **options):
        user = User.objects.create(
            username=self.fake.first_name(),
            password='T13431344'
        )

        for _ in range(10):
            Todo.objects.create(
                user=user,
                task=self.fake.paragraph(nb_sentences=1),
                complete=random.choice(complete_choices),
            )

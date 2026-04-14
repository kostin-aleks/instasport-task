"""
Manage command to fill tables with test data
"""

from faker import Faker
import random
import re

from django.conf import settings
from django.core.management.base import BaseCommand

from instasport.locations.models import Country, City, SportClub, SportHall
from instasport.users.models import Person
from instasport.training.models import Sport, SportsTraining

TEST_PREFIX = "test-"

TEST_DATA = {
    "country": [
        {"name": "Украина", "iso": "UA"},
    ],
    "city": [
        {"name": "Харьков", "country": "UA"},
        {"name": "Полтава", "country": "UA"},
    ],
    "sportclub": [
        {
            "city": "kharkov",
            "name": "АдреналинКлуб",
            "description": """
                Спортивный клуб, специализирующийся на функциональном тренинге,
                кроссфите и силовых единоборствах.""",
            "halls": [
                {
                    "name": "Большой зал",
                    "description": """Много свободного пространства, специфическое оборудование
                        (гири, канаты, тумбы, штанги, кольца).
                        Тренировки проходят группами высокой интенсивности.""",
                },
            ],
        },
        {
            "city": "kharkov",
            "name": "Сила и Грация",
            "description": """
                Тренажерный зал с зоной свободных весов, кардио-зоной и
                залом групповых программ (йога, пилатес, стретчинг""",
            "halls": [
                {
                    "name": "Тренажерный зал",
                    "description": """
                        Наличие зон со свободными весами (гантели, штанги),
                        силовыми тренажерами и кардиозоны
                        (беговые дорожки, эллипсы).
                        Фокус на самостоятельные тренировки.""",
                },
                {
                    "name": "Студия",
                    "description": """
                        Высокая квалификация тренеров, камерная атмосфера,
                        фокус на групповые тренировки""",
                },
            ],
        },
        {
            "city": "poltava",
            "name": "Железная Воля",
            "description": """
                Хардкорный тренажерный зал для бодибилдинга и пауэрлифтинга
                с профессиональным оборудованием.""",
            "halls": [
                {
                    "name": "Тренажерный зал",
                    "description": """
                        Современные тренажеры, бассейны, дизайнерские интерьеры,
                        дополнительные услуги""",
                }
            ],
        },
    ],
    "coach": ["coach1", "coach4", "coach10", "coach5", "coach77"],
    "sport": ["Аэробика", "Кроссфит", "Бодибилдинг", "Йога"],
}


def create_day_schedule(
    club: SportClub, weekday: int, sport: Sport, coach: Person
) -> None:
    """create schedule of trainings for one day of week"""

    _TIME = ({"start": "09:30", "end": "12:00"}, {"start": "17:30", "end": "20:00"})
    for hall in club.sporthall_set.filter(is_active=True):
        for time_item in _TIME:
            _ = SportsTraining.objects.create(
                sporthall=hall,
                weekday=weekday,
                coach=coach,
                sport=sport,
                start_time=time_item["start"],
                end_time=time_item["end"],
            )


def create_schedule():
    """create test schedule of trainings"""

    clubs = SportClub.objects.filter(slug__startswith=TEST_PREFIX)
    coaches = list(
        Person.objects.filter(
            role=Person.Role.COACH, is_active=True, username__startswith="coach"
        )
    )
    sports = list(Sport.objects.all())

    # remove test schedule
    SportsTraining.objects.filter(sporthall__club__in=clubs).delete()
    for club in clubs:
        print(club.slug)

        for wd in range(1, 8):
            coach = random.choice(coaches)
            sport = random.choice(sports)
            create_day_schedule(club, wd, sport, coach)


def create_admin():
    """create test admin"""
    fake = Faker("ru_RU")

    password = settings.SUPERUSER_PASSWORD
    username = settings.SUPERUSER_USERNAME
    email = fake.email()

    if not Person.objects.filter(username=username).first():
        admin = Person.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
    admin.first_name, admin.middle_name, admin.last_name = fake.name().split()
    admin.save()


class Command(BaseCommand):
    """
    This manage command fills tables
    with test data
    """

    help = """Create test training data."""

    def handle(self, *args, **kwargs):

        fake = Faker("ru_RU")

        # country
        for item in TEST_DATA["country"]:
            country, created = Country.objects.get_or_create(iso=item["iso"].upper())
            country.name = item["name"]
            country.save()

        # cities
        for item in TEST_DATA["city"]:
            city, created = City.objects.get_or_create(
                name=item["name"],
                country=Country.objects.get(iso=item["country"].upper()),
            )

        # clubs with sporthalls
        for item in TEST_DATA["sportclub"]:
            club, created = SportClub.objects.get_or_create(
                name=item["name"], city=City.objects.get(slug=item["city"])
            )
            description = re.sub(r"\s{2,}", " ", item["description"])
            club.description = description.strip()
            club.save()
            if not club.slug.startswith(TEST_PREFIX):
                club.slug = TEST_PREFIX + club.slug
                club.save()

            for hall in item["halls"]:
                sporthall, created = SportHall.objects.get_or_create(
                    club=club, name=hall["name"]
                )
                description = re.sub(r"\s{2,}", " ", hall["description"])
                sporthall.description = description.strip()
                sporthall.save()

        # coaches
        for item in TEST_DATA["coach"]:
            coach, created = Person.objects.get_or_create(
                username=item, role=Person.Role.COACH
            )
            coach.email = fake.email()
            coach.first_name, coach.middle_name, coach.last_name = fake.name().split()
            coach.save()

        # sport
        for item in TEST_DATA["sport"]:
            sport, created = Sport.objects.get_or_create(name=item)

        # trainings
        create_schedule()

        # admin
        create_admin()

        print("All test objects added.")

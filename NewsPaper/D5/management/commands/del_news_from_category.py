from django.core.management.base import BaseCommand, CommandError
from D5.models import Post, Category
from django.core.exceptions import ObjectDoesNotExist

class Command(BaseCommand):
    help = 'Удаляет все статьи в введённой категории'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(f'Вы правда хотите удалить все статьи в категории {options["category"]}? yes/no: ')
        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Действие отменено'))
        else:
            name = Category.objects.values_list('name_category', flat=True)
            try:
                category = Category.objects.get(name_category=options['category'])
                Post.objects.filter(category==category).delete()
                self.stdout.write(self.style.SUCCESS(f'Удалены все статьи из категории {category.name_category}'))
            except ObjectDoesNotExist:
                self.stdout.write(self.style.ERROR(f'Не найдена категория, существующие категории {name}'))

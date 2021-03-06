from user_api.models import User
from django.core.management.base import BaseCommand
from dashboard.models import Teacher
import  logging


logger = logging.getLogger(__name__)
class Command(BaseCommand):
    help = 'create users for all user'


    def handle(self, *args, **kwargs):
        try:
            ''' NOTE : fetch all teachers '''
            teacher_queryset = Teacher.objects.all()
            for teacher in teacher_queryset:
                username = teacher.email
                split_value = username.split('.')
                password = f'{split_value[0]}@{split_value[0]}' #create password like nadeem@nadeem  from nadeem.ali@stacfucion.io

                ''' NOTE : Check user already exists '''
                if User.objects.filter(username=username).exists():
                    logger.info(f'{username}  is already exists.')
                    continue

                '''TODO : create user for every teachers'''
                user = User.objects.create_user(username=username,password=password.lower(),is_teacher=True)

                logger.info(f'''
                        username : {username},
                        password : {password}
                        ''')

        except Exception as e:
            logger.info(f'Error : {e}...')


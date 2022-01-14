from django.contrib.auth.models import  Group , Permission
from user_api.models import User
from django.core.management.base import BaseCommand
import  logging
from django.core.exceptions import ValidationError

logger = logging.getLogger(__name__)
class Command(BaseCommand):
    help = 'create users for mainter user'


    def handle(self, *args, **kwargs):
        try:
            ''' NOTE : Enter Username or Password '''

            username =  str(input("enter username : "))
            password =  str(input("enter password : "))
            repassword =  str(input("confirm password : "))


            special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"

            ''' NOTE : Check Password are same or Not '''
            if password != repassword:
                logger.info('passwords are\'nt matched !!!')
                return 'passwords are\'nt matched !!!'

            ''' NOTE : Check Password have any digit '''
            if not any(char.isdigit() for char in password):
                return 'Password must contain at least 1 digit.'

            ''' NOTE : Check Password have any alphabatic '''
            if not any(char.isalpha() for char in password):
                return 'Password must contain at least 1 letter.'

            ''' NOTE : Check Password have any special character '''
            if not any(char in special_characters for char in password):
                return 'Password must contain at least 1 special character.'



            ''' NOTE : Check user already exists '''
            if User.objects.filter(username=username).exists():
                logger.info(f'{username}  is already exists.')
                return f'{username}  is already exists !!!'

            '''TODO : create user for every teachers'''
            user = User.objects.create_user(username=username,password=password.lower())

            print("\nuser created successfully...")
            group = Group.objects.get_or_create(name='mainter')  # group create or get



            '''NOTE : get substitution perissions'''
            all_permissions = Permission.objects.filter(content_type__app_label='substitution',
                                                        content_type__model='substitution')
            group = Group.objects.get(name='mainter')  # group get for add user

            try:
                ''' TODO : Give permissions to mainter group '''
                for permission in all_permissions:
                    group.permissions.add(permission)

            except:
                pass



            user.groups.add(group) #add user to group
            logger.info(f''' User `{user.username}` added to group `{group.name}` ''')
            print(f'''User `{user.username}` added to group `{group.name}` ''')

        except Exception as e:
            logger.info(f'Error : {e}...')


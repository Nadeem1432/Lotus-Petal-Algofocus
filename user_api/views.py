# from django.shortcuts import render

import logging
from datetime import *

from dashboard.models import Teacher
from django.contrib import auth
from django.utils import timezone
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import LoginSerializer ,GoogleLoginSerializer

# import google-auth
from google.oauth2 import id_token
from google.auth.transport import requests
from user_api.models import User



# Get an instance of a logger
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s-%(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')



'''
loginApi for share the content of existing logged user .
basically it developed for ANDROID APP  of Lotus Petal 
'''
# TODO: MODIFICATION REQUIRED AND ADD SERIALIZER OF TEACHER

# New code
class LoginAPI(APIView):

    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            request_data = serializer.data

            # request parameters
            username = request_data.get('username', 'username not found!!!')
            password = request_data.get('password', 'password not found!!!')

            ''' let a var to make caseSensitive for username '''
            caseSensitiveUsername =  username

            ''' check user is exist or not based on casesensitive username '''
            try:
                findUser = User.objects.get(username__iexact=username)
            except User.DoesNotExist:
                findUser = None


            ''' TODO: authentication with creds'''
            if findUser:
                caseSensitiveUsername = findUser.username
                user = auth.authenticate(username=caseSensitiveUsername, password=password.lower())

                ''' TODO : if user is authenticated we should check user is teacher or admin'''
                if user:
                    teacher = user.is_teacher
                    admin   = user.is_admin

                    ''' TODO : if user is teacher send response data from Teacher model based on teacher email'''
                    if teacher:

                        teacher_data = Teacher.objects.get(email__iexact=caseSensitiveUsername)  # fetch authenticated user's data

                        user_id = teacher_data.classe_365_id  # user's id
                        first_name = teacher_data.first_name  # user's first name
                        last_name = teacher_data.last_name  # user's last name
                        full_name = first_name + ' ' + last_name
                        user_email = teacher_data.email  # user's email

                        Token = RefreshToken.for_user(user).access_token  # create a token for authenticated user
                        Expiry_time = ((timezone.now()) + timedelta(days=15)).strftime(
                            "%m/%d/%Y, %I:%M:%S %p")  # get time next 2 hours
                        logger.info("successfully logged in as a teacher")

                        return Response({"detail": "successfully logged in",
                                         "Token": str(Token),
                                         "Expiry": "Token will be Expire at " + Expiry_time,
                                         "user_data":
                                             {
                                                 "user_type": "Teacher",
                                                 "user_id": user_id,
                                                 "user_name": full_name,
                                                 "user_designation": None,
                                                 "user_email": user_email,
                                                 "user_phone": None,

                                             },

                                         "error_details ": None

                                         }
                                        , status=200)


                        ''' TODO if user is admin then send response data from User model'''
                    elif admin:
                        print(' user is admin  line 110')

                        user_id = findUser.id  # user's id
                        first_name = findUser.first_name  # user's first name
                        last_name = findUser.last_name  # user's last name
                        full_name = first_name + ' ' + last_name
                        user_email = findUser.username  # user's username ,beacause sometimes email can be  so here we passing username as email

                        Token = RefreshToken.for_user(user).access_token  # create a token for authenticated user
                        Expiry_time = ((timezone.now()) + timedelta(days=15)).strftime(
                            "%m/%d/%Y, %I:%M:%S %p")  # get time next 2 hours
                        logger.info("successfully logged in")

                        return Response({"detail": "successfully logged in",
                                         "Token": str(Token),
                                         "Expiry": "Token will be Expire at " + Expiry_time,
                                         "user_data":
                                             {
                                                 "user_type": "Admin",
                                                 "user_id": user_id,
                                                 "user_name": full_name,
                                                 "user_designation": None,
                                                 "user_email": user_email,
                                                 "user_phone": None,

                                             },

                                         "error_details ": None

                                         }
                                        , status=200)

                        '''if any user have no role like  teacher or admin , send a simple unauthorized response for that user'''
                    else:

                        return Response({
                            'app_code': 1,
                            'error_code': 3,
                            'detail': "User Exist but any role not allowed for this user like Admin or Teacher",
                            'log_id': "",
                            'display': True
                        }, status=403)

                    ''' Condition for  , User is present but unauthenticated'''
                else:

                    return Response({
                        'app_code': 1,
                        'error_code': 2,
                        'detail': "Invalid Password",
                        'log_id': "",
                        'display': True
                    }, status=403)



                ''' Exception for unauthorized user  '''
            else:

                return Response({
                    'app_code': 1,
                    'error_code': 2,
                    'detail': "Invalid Username or Password",
                    'log_id': "",
                    'display': True
                }, status=403)









# NOTE : old login api code
# class LoginAPI(APIView):
#
#     permission_classes = [AllowAny]
#     serializer_class = LoginSerializer
#
#     def post(self, request, *args, **kwargs):
#         serializer = LoginSerializer(data=request.data)
#
#         if serializer.is_valid():
#             user_dicionary = serializer.data
#
#             username = user_dicionary.get('username', 'username not found!!!')
#             password = user_dicionary.get('password', 'password not found!!!')
#
#             # here main work work of authentication
#             # user = auth.authenticate(username=username, password=password)
#
#             split_value = username.split('.')
#             password2 = f'{split_value[0]}@{split_value[0]}' #password according to username
#
#
#
#             user_present     =  User.objects.filter(username__iexact=username).exists()
#
#
#
#             try:
#
#                 # if user is exists  return it's response
#                 # if user:
#
#                 if user_present and password==password2:
#                     user = User.objects.get(username__iexact=username)
#
#                     if Teacher.objects.filter(email__iexact=username).exists():
#                         user_data = Teacher.objects.get(email__iexact=username)  # fetch authenticated user's data
#                         user_id = user_data.classe_365_id  # user's id
#                         first_name = user_data.first_name  # user's first name
#                         last_name = user_data.last_name  # user's last name
#                         full_name = first_name + ' ' + last_name
#                         user_email = user_data.email  # user's email
#                         user_type = user.is_admin  # get user type
#
#                         Token = RefreshToken.for_user(user).access_token  # create a token for authenticated user
#                         Expiry_time = ((timezone.now()) + timedelta(days=15)).strftime("%m/%d/%Y, %I:%M:%S %p")  # get time next 2 hours
#                         # Configured already in settings.py for token's lifetime
#                         logger.info("successfully logged in")
#                         return Response({"detail": "successfully logged in",
#                                          # "code":"200",
#                                          "Token": str(Token),
#                                          "Expiry": "Token will be Expire at " + Expiry_time,
#                                          "user_data":
#                                              {
#                                                  "user_type": "Admin" if user_type else "Teacher",
#                                                  "user_id": user_id,
#                                                  "user_name": full_name,
#                                                  "user_designation": None,
#                                                  "user_email": user_email,
#                                                  "user_phone": None,
#
#                                              },
#
#                                          "error_details ": None
#
#                                          }
#                                         , status=200)
#                     else:
#                         user_id = user.id  # user's id
#                         first_name = user.first_name  # user's first name
#                         last_name = user.last_name  # user's last name
#                         full_name = first_name + ' ' + last_name
#                         user_email = user.email  # user's email
#
#                         Token = RefreshToken.for_user(user).access_token  # create a token for authenticated user
#                         Expiry_time = ((timezone.now()) + timedelta(days=15)).strftime(
#                             "%m/%d/%Y, %I:%M:%S %p")  # get time next 2 hours
#
#                         user_type = user.is_admin  # get user type
#                         return Response({"detail": "successfully logged in",
#                                          # "code":"200",
#                                          "Token": str(Token),
#                                          "Expiry": "Token will be Expire at " + Expiry_time,
#                                          "user_data":
#                                              {
#                                                  "user_type": "Admin" if user_type else "Teacher",
#                                                  "user_id": user_id,
#                                                  "user_name": full_name,
#                                                  "user_designation": None,
#                                                  "user_email": user_email,
#                                                  "user_phone": None,
#
#                                              },
#
#                                          "error_details ": None
#
#                                          }
#                                         , status=200)
#
#
#                 else:
#                     # 'Doesn\'t Exists User'
#                     return Response({
#                         'app_code': 1,
#                         'error_code': 2,
#                         'detail': "Invalid Username or Password",
#                         'log_id': "",
#                         'display': True
#                     }, status=403)
#
#             except Exception as e:
#                 logger.error(f'Error: {e}')
#                 return Response({"detail": "Some handled error in API ",
#                                  'app_code': 1,
#                                  'error_code': 1,
#                                  # 'detail': "UserID or password not sent",
#                                  'log_id': "",
#                                  'display': True,
#                                  'Error': f'{e}'
#
#                                  }, status=400)
#
#         else:
#             return Response({"error": serializer.errors}, status=400)








# +++++++++++++++++++++++++++____GOOGLE LOGIN API_____+++++++++++++++++++++++#

'''
Google loginApi for share the content of existing logged user .
basically it developed for ANDROID APP  of Lotus Petal 
'''
# TODO: MODIFICATION REQUIRED AND ADD SERIALIZER OF TEACHER
class GoogleLoginAPI(APIView):

    permission_classes = [AllowAny]
    serializer_class = GoogleLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = GoogleLoginSerializer(data=request.data)

        if serializer.is_valid():
            user_dicionary = serializer.data

            username = user_dicionary.get('username', 'username not found!!!')
            token_id = user_dicionary.get('token_id', 'token_id not found!!!')
            client_id = user_dicionary.get('user_id', 'user_id not found!!!')

            # NOTE : check user is exist or not in db
            is_user_exists = User.objects.filter(username=username).exists()

            


            try:

                # NOTE :  user get if exists
                if is_user_exists:
                    user = User.objects.get(username=username)

                    # NOTE :  check google token verification 
                    idinfo = id_token.verify_oauth2_token(token_id, requests.Request(), client_id)

                    if Teacher.objects.filter(email=username).exists():
                        user_data = Teacher.objects.get(email=username)  # fetch authenticated user's data

                        user_id = user_data.classe_365_id  # user's id
                        first_name = user_data.first_name  # user's first name
                        last_name = user_data.last_name  # user's last name
                        full_name = first_name + ' ' + last_name
                        user_email = user_data.email  # user's email
                        user_type = user.is_staff  # get user type

                        Token = RefreshToken.for_user(user).access_token  # create a token for authenticated user
                        Expiry_time = ((timezone.now()) + timedelta(hours=2)).strftime("%m/%d/%Y, %I:%M:%S %p")  # get time next 2 hours
                        # Configured already in settings.py for token's lifetime

                        logging.info(f" {username} successfully  logged in.")

                        return Response({"detail": "successfully logged in",
                                         "Token": str(Token),
                                         "Expiry": "Token will be Expire at " + Expiry_time,
                                         "user_data":
                                             {
                                                 "user_type": "Admin" if user_type else "Teacher",
                                                 "user_id": user_id,
                                                 "user_name": full_name,
                                                 "user_designation": None,
                                                 "user_email": user_email,
                                                 "user_phone": None,

                                             },

                                         "error_details ": None

                                         }
                                        , status=200)
                                    

                    else:
                        logging.error("User Doesn't exists")

                        return Response(
                            {
                                    'app_code': 3,
                                    'error_code': 3,
                                    'detail': "User Doesn't exists",
                                    'log_id': "",
                                    'display': True
                                }, 
                                status=403
                            )
                else:
                    
                    return Response(
                        {
                                'app_code': 3,
                                'error_code': 3,
                                'detail': "Invalid username !!!",
                                'log_id': "",
                                'display': True
                            }, 
                            status=403
                        )




            except ValueError:
                return Response({
                        'app_code': 1,
                        'error_code': 2,
                        'detail': "Invalid  Token or Expired ,check  user_id. ",
                        'log_id': "",
                        'display': True
                    }, status=403)
                
                


        else:
            logging.error(f"Error :  {serializer.errors} .")
            return Response({"error": serializer.errors}, status=400)




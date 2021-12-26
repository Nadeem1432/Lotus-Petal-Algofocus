

# class AttendenceSerializer(serializers.ModelSerializer):
#
#     date = serializers.SerializerMethodField('get_date')
#     class Meta:
#         model = Attendence_Data
#         fields = ['student_id','admission_no','section_id','status','date']
#
#     def create(self, validated_data):
#         attendences = Attendence_Data.objects.create(**validated_data)
#         return attendences
#
#     def get_date(self):
#         date = datetime.datetime.now().strftime('%Y-%m-%d') #get time next 2 hours
#         return date




#
# class AttendenceSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Attendence_Data
#         fields = ['student_id','subject_id','section_id','status']
#
#     # def create(self, validated_data):
#     #     attendences = Attendence_Data.objects.create(**validated_data)
#     #     return attendences
#
#     def create(self, validated_data):
#         user = Attendence_Data.objects.create(validated_data['id2'], validated_data['email'], validated_data['name'])
#         return user  # it will be return  created user







# class TeacherViewset(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JWTAuthentication]

#     queryset = Teacher.objects.all()
#     serializer_class = GetAllTeacherSerializer





# # Teacher list  Serializer
# class GetAllTeacherSerializer(serializers.HyperlinkedModelSerializer):
#     teacher_id = serializers.CharField(source='classe_365_id')  #source use for changed the name of model attribute
#     teacher_name = serializers.CharField(source='fullname')
#     teacher_email = serializers.CharField(source='email')
#     # teacher_subjects = serializers.CharField(source='subjects')


#     class Meta:
#         model = Teacher
#         fields = ['url','teacher_id', 'teacher_name','teacher_email','subjects' ]
#         extra_kwargs = {"success": 200, "error_code":0}







#======================TimeTable API=================================#
# from dashboard.models import Claas, Section

# from .serializers import ClassTimeTableSerializer, SectionTimeTableSerializer

#TESTING CODE
# class SectionTimeTableAPI(viewsets.ModelViewSet):
#     permission_classes = [AllowAny,]
#     queryset = Section.objects.all()
#     serializer_class = SectionTimeTableSerializer


# class TimeTableAPI(viewsets.ModelViewSet):
#     permission_classes = [AllowAny,]
#     queryset = Claas.objects.all()
#     serializer_class = ClassTimeTableSerializer





# --------------------------

# class Get_All_Students(APIView):
#     authentication_classes = [JWTAuthentication]

#     permission_classes = [IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         request_data = request.data
#         # pass data for save the history of class start  time
#         # class_id          = request_data.get('class_id')
#         section_id = request_data.get('section_id')
#         try:

#             if section_id:  # this condition for both parameter's value in not None

#                 querySet = Student.objects.filter(section__section_id=section_id,
#                                                   ).values()

#                 students_list = [i for i in querySet]
#                 if students_list:

#                     return Response(students_list, status=200)
#                 else:
#                     return Response({"details": "Sorry , There is No student in thins class."}, status=200)

#             else:
#                 return Response({"details": "Provide a valid parameters.",
#                                  'app_code': 1,
#                                  'error_code': 2,
#                                  'detail': "Please enter required feilds",
#                                  'display': True

#                                  }, status=400)


#         except Exception as e:
#             return Response({"details": "Some handled error in API",
#                              'app_code': 1,
#                              'error_code': 1,
#                              'detail': "Some Went Wrong in API",
#                              'log_id': "",
#                              'display': True,

#                              }, status=400)




# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------





# class GetAllStudentForClass(serializers.ModelSerializer):
#     class Meta:
#         model = Student
#         fields = '__all__' #get all fields



# class AttendenceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Attendence_Data
#         fields = '__all__'




# #====================== Time Table Serailizer =========================

# # section serializer
# class SectionTimeTableSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Section
#         fields = ['section_id','section_name']

# # class serializer
# class ClassTimeTableSerializer(serializers.ModelSerializer):
#     sections = SectionTimeTableSerializer(many=True,read_only=True) # get all properties of section serializer
#     # print(sections)

#     class Meta:
#         model = Claas
#         fields = ('claas_id','claas_name','sections') #parse in class's serializer for interface



# --------------------------------------------------------------------------------




# class Attendence_Data(models.Model):
#     # classe 365's id   ( id2  bcoz id is already default defined)
#     id2 = models.CharField(max_length=20)
#     # id of the student
#     student_id = models.CharField(max_length=50)
#     # admission number of student
#     admission_no = models.CharField(max_length=50)
#     # email of the email
#     email = models.CharField(max_length=120)

#     name = models.CharField(max_length=150)
#     # section id
#     section_id = models.CharField(max_length=10)

#     status = models.CharField(max_length=10)

#     def __str__(self):
#         return self.name





# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------

#header for token and api url
# header = {"Authorization":"Basic ZGVtbzorQENlOUx6Unl3YjVtNXE2"}
# api_url = 'https://demo.classe365.com/rest/manageAttendance'



# class AttendanceAPI(APIView):
#     permission_classes = (IsAuthenticated,)
#     serializer_class = AttendenceSerializer

#     def post(self, request, *args, **kwargs):
#         if request.method=='POST':
#             serializer = AttendenceSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save()

#                 Attendence_list = Attendence_Data.objects.all().values()

#                 # iterate for get all saved data in Attendence table
#                 for Attendence in Attendence_list:
#                     student_id   = Attendence.get('student_id',None)
#                     section_id   = Attendence.get('section_id',None)
#                     status       = Attendence.get('status',None)

#                     # get claas_id by given section_id
#                     if Section.objects.filter(section_id = section_id).exists() and Subject.objects.filter(section__section_id=section_id).exists():
#                         claas_id_object = Section.objects.get(section_id = section_id)
#                         class_id = claas_id_object.claas.claas_id

#                         # get subject_id by given section_id
#                         subject_id_object = Subject.objects.get(section__section_id=section_id)
#                         subject_id = subject_id_object.subject_id

#                         # get date
#                         date = datetime.datetime.now().strftime('%Y-%m-%d') #get time next 2 hours

#                         data = {
#                             "class_id":class_id ,
#                             "section_id":section_id ,
#                             "subject_id":subject_id ,
#                             "session_id":None,
#                             "date":date,
#                             "working":1,
#                             "attendance_data":{
#                                                 student_id:{
#                                                             "status":"p" if status=="present" else "a", #check if status is 'present' then 'p' else 'a'
#                                                             "commment":None # None for now
#                                                             }
#                                                 }
#                                 }

#                         #here hit class365's API
#                         result = requests.post(url=api_url,data=data,headers=header)
#                         request_status_code = result.status_code
#                         if request_status_code==200:

#                             logging.info("Success!")
#                             return Response( {"details":result.json()}, status=200)
#                         else:
#                             logging.error("Error occured while hit class365 API!!!")
#                             return Response( {"details":"attendence didn't send to class365"} , status=400)

#                     # This condition for when section_id is wrong entered by teacher
#                     else:
#                         return Response({"details": "Class365 API didn't hit."}, status=400)
#                     # return Response(serializer.data , status =200)
#             else:
#                 return Response({"error":serializer.errors},status=400)














#============================ End Serialized Login API Code =========================================









#============================= START / STOP CLASS API CODE START ================================================
# # StartClass Api
# class StartClass(APIView):
#     permission_classes = [AllowAny]
#
#     def post(self, request, *args, **kwargs):
#         request_data = request.data
#         # pass data for save the hostory of class start  time
#         class_id = request_data.get('class_id')
#         class_name = request_data.get('class_name')
#         teacher_id = request_data.get('teacher_id')
#         teacher_name = request_data.get('teacher_name')
#         class_section = request_data.get('class_section')
#         start_time = request_data.get('start_time')
#
#         try:
#             # check all fields are not None
#             if class_id and class_name and teacher_id and teacher_name and class_section and start_time:  # this condition for both parameter's value in not None
#
#                 start_time_model_object = Start_class(class_id=class_id,
#                                                       class_name=class_name,
#                                                       teacher_id=teacher_id,
#                                                       teacher_name=teacher_name,
#                                                       class_section=class_section,
#                                                       start_time=start_time
#                                                       )
#                 start_time_model_object.save()  # save here
#                 return Response({"details": "successfully saved Start Class history...",
#                                  "app_code": 1,
#                                  "error_code": None,
#                                  "error_details ": None
#
#                                  }
#                                 , status=200)
#
#             else:
#                 return Response({"details": "Provide a Valid Parameters",
#                                  'app_code': 1,
#                                  'error_code': 2,
#                                  'detail': "Please enter required feilds",
#                                  'log_id': "",
#                                  'display': True
#
#                                  }, status=400)
#
#
#         except Exception as e:
#             return Response({"details": "Some handled error in API",
#                              'app_code': 1,
#                              'error_code': 1,
#                              'detail': "Something Went Wrong in API",
#                              'log_id': "",
#                              'display': True,
#
#                              }, status=400)
#
#         # StartClass Api
#
#
# class StopClass(APIView):
#     permission_classes = [AllowAny]
#
#     def post(self, request, *args, **kwargs):
#         request_data = request.data
#         print('Before success')
#         # pass data for save the history of class start  time
#         class_id = request_data.get('class_id')
#         class_name = request_data.get('class_name')
#         teacher_id = request_data.get('teacher_id')
#         teacher_name = request_data.get('teacher_name')
#         class_section = request_data.get('class_section')
#         stop_time = request_data.get('stop_time')
#         try:
#
#             if class_id and class_name and teacher_id and teacher_name and class_section and stop_time:  # this condition for both parameter's value in not None
#
#                 stop_time_model_object = Stop_class(class_id=class_id,
#                                                     class_name=class_name,
#                                                     teacher_id=teacher_id,
#                                                     teacher_name=teacher_name,
#                                                     class_section=class_section,
#                                                     stop_time=stop_time
#                                                     )
#                 stop_time_model_object.save(),
#
#                 return Response({"details": "Successfully saved Stop Class history...",
#                                  # "code":"200",
#                                  "app_code": 1,
#                                  "error_code": None,
#                                  "error_details ": None
#
#                                  }
#                                 , status=200)
#
#             else:
#                 return Response({"details": "Provide a valid parameters.",
#                                  'app_code': 1,
#                                  'error_code': 2,
#                                  'detail': "Please enter required feilds",
#                                  'display': True
#
#                                  }, status=400)
#
#
#         except Exception as e:
#             return Response({"details": "Some handled error in API",
#                              'app_code': 1,
#                              'error_code': 1,
#                              'detail': "Some Went Wrong in API",
#                              'log_id': "",
#                              'display': True,
#
#                              }, status=400)
#
#         # Api for get all students for a particular class


#============================= START / STOP CLASS API CODE END ================================================



#============================HARD CODE API FOR ATTENDENCE========================================

# # Api for Add attendace
# class AttendanceAPI(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes =[IsAuthenticated]


#     def post(self, request, *args, **kwargs):
#         request_data    = request.data
#         #pass data for add attendance
#         id          = request_data.get('id')
#         student_id  = request_data.get('student_id')
#         admission_no= request_data.get('admission_no')
#         email       = request_data.get('email')
#         name        = request_data.get('name')
#         section_id  = request_data.get('section_id')
#         status      = request_data.get('status')

#         #header for token and api url
#         header = {"Authorization":"Basic ZGVtbzorQENlOUx6Unl3YjVtNXE2"}
#         api_url = 'https://demo.classe365.com/rest/manageAttendance'


#         try:

#             if id and student_id and admission_no and email and name and status and section_id: #this condition for both parameter's value in not None

#                 #save attendece data
#                 Attendence_Data_Table = Attendence_Data(id2=id ,
#                                             student_id =student_id ,
#                                              admission_no=admission_no ,
#                                               email=email , name = name ,
#                                                section_id = section_id ,
#                                                 status=status)
#                 Attendence_Data_Table.save()
#                 # fetch all data for attendence
#                 Attendence_list = Attendence_Data.objects.all().values()

#                 # iterate for get all saved data in Attendence table
#                 for Attendence in Attendence_list:
#                     student_id   = Attendence.get('student_id',None)
#                     admission_no = Attendence.get('admission_no',None)
#                     section_id   = Attendence.get('section_id',None)
#                     status       = Attendence.get('status',None)

#                     # line for debugging
#                     # print(f'\n\n\n{id}\n{student_id}\n{admission_no}\n{email}\n{name}\n{section_id}\n{status}')

#                     # get claas_id by given section_id
#                     if Section.objects.filter(section_id = section_id).exists() and Subject.objects.filter(section__section_id=section_id).exists():
#                         claas_id_object = Section.objects.get(section_id = section_id)
#                         class_id = claas_id_object.claas.claas_id

#                         # get subject_id by given section_id
#                         subject_id_object = Subject.objects.get(section__section_id=section_id)
#                         subject_id = subject_id_object.subject_id

#                         # get date
#                         date = datetime.datetime.now().strftime('%Y-%m-%d') #get time next 2 hours

#                         data = {
#                             "class_id":class_id ,
#                             "section_id":section_id ,
#                             "subject_id   ":subject_id ,
#                             "session_id":None,
#                             "date":date,
#                             "working":1,
#                             "attendance_data":{
#                                 student_id:{
#                                     "status":"p" if status=="present" else "a", #check if status is 'present' then 'p' else 'a'
#                                     "commment":None # None for now
#                                             }
#                                 }

#                         }
#                         #here hit class365's API

#                         result = requests.post(url=api_url,data=data,headers=header)
#                         request_status_code = result.status_code
#                         if request_status_code==200:

#                             logging.error("Success!")
#                             return Response( {"details":"success"}, status=200)
#                         else:
#                             logging.error("Error occured while hit class365 API!!!")
#                             return Response( {"details":"attendence didn't send to class365"} , status=400)

#                     # This condition for when section_id is wrong entered by teacher
#                     else:
#                         # # get date
#                         # date = datetime.datetime.now().strftime('%Y-%m-%d') #get time next 2 hours


#                         # #data for api
#                         # data = {
#                         #     "class_id":None,
#                         #     "section_id":section_id if section_id else None,
#                         #     "subject_id":None,
#                         #     "session_id":None,
#                         #     "date":date,
#                         #     "working":1,
#                         #     "attendance_data":{
#                         #         student_id if student_id  else None:{
#                         #             "status":"p" if status=="present" else "a",
#                         #             "commment":None # None for now
#                         #                     }
#                         #         }

#                         # }

#                         # #here hit class365's API

#                         # result = requests.post(url=api_url,data=data,headers=header)
#                         # request_status_code = result.status_code
#                         # if request_status_code==200:
#                         #     logging.error(f"Error occured while fetching latest ANPR. Error : {e}")
#                         #     return Response( {"details":"success but section_id , class_id didn't get."}, status=200)
#                         # else:
#                         logging.warning(f"Success but section_id , class_id didn't matched from sections")
#                         return Response( {"details":"data not send to class365"}, status=400)

#             else:

#                 logging.error("parameters are'nt provided !!! ")
#                 return Response({ "details": "Provide a valid parameters.",
#                                         'app_code' : 1,
#                                         'error_code':2,
#                                         'detail':"Please enter required feilds",
#                                         'display':True

#                                     }, status=400)


#         except Exception as e:
#             logging.error(f"Error occured while Hit 'Add Attendence API' . Error : {e}")
#             return Response({ "details": "Some handled error in API",
#                                 'app_code' : 1,
#                                 'error_code':1,
#                                 'detail':"Some Went Wrong in API",
#                                 'log_id':"",
#                                 'display':True,


#                                 } , status=400)





# ================ SERIALIZER METHOD =================





#=========METHOD 1=============================

# from rest_framework.decorators import api_view
#
# @api_view(['POST'])
# def AttendanceAPI(request):
#     if request.method=='POST':
#         serializer = AttendenceSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data , status =200)
#         else:
#             return Response({"error":serializer.errors})
















#=====================METHOD 2===================================





















#============================= HARD CODE LOGIN API ================================================
# # Login Api
# class LoginAPI(APIView):
#     permission_classes = [AllowAny]
#
#     def post(self, request, *args, **kwargs):
#         request_data = request.data
#         # pass credentials for authentication user is exists or not
#         username = request_data.get('username')
#         password = request_data.get('password')
#
#         # get value of username & password for apply validation if username is not blank
#         # username_value = request_data['username']
#         # password_value = request_data['password']
#         # length_of_body = len(request_data)
#         try:
#
#             if username and password:  # this condition for both parameter's value in not None
#
#                 user = auth.authenticate(username=username, password=password)  # here main work work of authentication
#
#                 # if user is not None: #if user is exists  return it's response
#                 if user:  # if user is exists  return it's response
#                     if Teacher.objects.filter(email=username.lower()).exists():
#                         user_data = Teacher.objects.get(email=username.lower())  # fetch authenticated user's data
#                         user_id = user_data.classe_365_id  # user's id
#                         first_name = user_data.first_name  # user's first name
#                         last_name = user_data.last_name  # user's last name
#                         full_name = first_name + ' ' + last_name
#                         user_email = user_data.email  # user's email
#                         user_type = user.is_staff  # get user type
#
#                         Token = RefreshToken.for_user(user).access_token  # create a token for authenticated user
#                         print(f'\n{Token}\n')
#                         Expiry_time = ((timezone.now()) + timedelta(hours=2)).strftime(
#                             "%m/%d/%Y, %I:%M:%S %p")  # get time next 2 hours
#                         # Configured already in settings.py for token's lifetime
#                         return Response({"details": "successfully logged in",
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
#                         return Response({
#                             'app_code': 3,
#                             'error_code': 3,
#                             'detail': "User is exists in UserList but not in teacher",
#                             'log_id': "",
#                             'display': True
#                         }, status=200)
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
#                     }, status=401)
#
#             else:
#                 return Response({"details": "Provide a Valid Cridientials"}, status=400)
#
#
#         except Exception as e:
#             return Response({"details": "Some handled error in API ",
#                              'app_code': 1,
#                              'error_code': 1,
#                              'detail': "UserID or password not sent",
#                              'log_id': "",
#                              'display': True,
#
#                              }, status=400)
        #     # return super(LoginAPI, self).post(request, format=None)
    #     return None
#======================End Hard Code Logi API =================================

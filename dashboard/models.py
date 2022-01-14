from django.db import models


class Claas(models.Model):

    # classe 365's class id
    claas_id = models.CharField(unique=True, max_length=50)
    # classe 365's class name
    claas_name = models.CharField(unique=True, max_length=50)
    # classe 365's class name original 
    claas_name_for_comparison = models.CharField(unique=True, max_length=50)
    
    def __str__(self):
        return self.claas_name


class ClaasAlias(models.Model):
    # Class code
    name = models.CharField(max_length=120, unique=True)
    # Class related to class code
    claas = models.OneToOneField(Claas, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Section(models.Model):

    # classe 365's section id
    section_id = models.CharField(unique=True, max_length=50)
    # classe 365's section name
    section_name = models.CharField(unique=False, max_length=50)

    section_name_for_comparison = models.CharField(unique=False, max_length=50)
    # many to one field, because a class can have multiple section
    claas = models.ForeignKey('Claas', on_delete=models.CASCADE)


    def __str__(self):
        return  f"{self.claas.claas_name} -- {self.section_name}"

    # the combination of these fields will be unique
    class Meta:
        unique_together = ("section_name", "claas")


class Subject(models.Model):

    # classe 365's subject id
    subject_id = models.CharField(unique=True, max_length=50)
    # classe 365's subject name
    subject_name = models.CharField(max_length=100)

    subject_name_for_comparison = models.CharField(max_length=100)
    # many to one field, because a section can have multiple subjects
    section = models.ForeignKey('Section', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.section.claas.claas_name} -- {self.section.section_name} -- {self.subject_name}"

    # the combination of these fields will be unique
    class Meta:
        unique_together = ("subject_name", "section")


class Teacher(models.Model):
    
    # classe 365's id of the teacher
    classe_365_id = models.CharField(unique=True, max_length=50)
    # email of the teacher
    email = models.EmailField(max_length=254)
    # first name of the teacher
    first_name = models.CharField(max_length=50)
    # last name of the teacher
    last_name = models.CharField(max_length=50)
    # Many to Many fiels with the subject, because a teacher can teach multiple subjects 
    # and also a subject can be taught by many teacher in same class
    subjects = models.ManyToManyField('Subject')

    #status for teacher is active or not
    # status =  models.BooleanField(default=True)

    def __str__(self):
        return self.first_name + self.last_name

    
class TeacherZoomDetails(models.Model):

    # to store teacher's zoom id 
    zoom_id = models.CharField(unique=True, max_length=100)
    teacher = models.OneToOneField('Teacher', on_delete=models.CASCADE)


class Student(models.Model):

    # classe 365's student id
    student_id = models.CharField(unique=True, max_length=50)
    # classe 365's admission no
    admission_no = models.CharField(unique=True, max_length=50)
    # email of the student
    # email = models.EmailField(unique=True, blank=True, null=True, max_length=254)
    email = models.EmailField(blank=True, null=True, max_length=254)
    # name of the student
    name = models.CharField(max_length=50)
    # Many to one field with section, because a section can have multiple students
    section = models.ForeignKey('Section', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class IncorrectTopic(models.Model):

    topic = models.CharField(max_length=100)

    meeting_id = models.CharField(unique=True, max_length=100)
    
    ''' NOTE: This will be the start time fetched when we get all the meetings of a teacher'''
    meeting_time = models.DateTimeField(blank=True, null=True)

    teacher_name = models.CharField(max_length=100, blank=True, null=True)

    created_on = models.DateTimeField(auto_now_add=True)

    updated_on = models.DateTimeField(auto_now=True)

    '''TODO: TEACHER EMAIL'''




# TODO: MODIFY IT AND RESOLVE THAT CORNER CASE
# TODO: REMOVE THE MODEL
# class IsAttendanceMarked(models.Model):

#     # the UUID of the instance of the meeting, it 'll be always unique
#     uuid = models.CharField(unique=True, max_length=50)
#     # topic name of the meeting
#     topic_name = models.CharField(max_length=100)
#     # boolean variable to know if the attendance of the meeting with this UUID has been updated in classe 365
#     is_marked = models.BooleanField(default=False)
    
#     # TODO:
#     student_json = models.JSONField(blank=True, null=True)

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     # TODO: MEETING TIME
#     meeting_time = models.DateTimeField(blank=True, null=True)
    
    
#     # we will also store if the topic name is as per the format described by us
#     # is_topic_name_correct = models.BooleanField(default=True)









# TODO: REMOVE THE MODEL
# class WrongEmail(models.Model):

#     topic = models.CharField(max_length=100)
#     user_name = models.CharField(max_length=50)
#     email = models.EmailField(blank=True, null=True, max_length=50)
#     meeting_uuid = models.CharField(max_length=50)
#     meeting_time = models.DateTimeField()
#     # teacher_email = 

#     created_on = models.DateTimeField(auto_now_add=True)
#     updated_on = models.DateTimeField(auto_now=True)

#     '''TODO: STUDENT CLASS'''
#     claas = models.CharField(max_length=50, blank=True, null=True)

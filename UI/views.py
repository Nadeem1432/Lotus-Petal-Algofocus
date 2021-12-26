from django.shortcuts import render , HttpResponse

# Create your views here.
def home(request):
    return  render(request , 'UI/index.html')

def privacy(request):
    return  render(request , 'UI/privacy_policy.html')

def index(request):
    return  render(request , 'build/index.html')

def timetable(request):
    return  render(request , 'build-timetable/index.html')

def attendance(request):
    return  render(request , 'build-attendance/index.html')
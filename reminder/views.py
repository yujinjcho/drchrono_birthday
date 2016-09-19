from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'reminder/index.html')

def birthdays(request):
    return render(request, 'reminder/birthdays.html')
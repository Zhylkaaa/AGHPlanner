from django.http import HttpResponse
from django.shortcuts import render
from .scripts.planer_script import plan_from_constraints
# Create your views here.


def index(request):
    template = 'planer/upload_csv.html'

    context = {
        'message': 'Upload CSV in following format: TODO',
    }

    if request.method == 'GET':
        return render(request, template, context)

    csv_file = request.FILES['file']

    result = plan_from_constraints(csv_file)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="result.csv"'

    result.to_csv(path_or_buf=response)
    return response

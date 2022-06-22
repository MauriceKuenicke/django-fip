from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import INCOMESOURCE, USER, PLAN
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.db.models import Sum
from .forms import CreatePlanForm
from django.utils import timezone




# Create your views here.
def index(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CreatePlanForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            plan_name = form.cleaned_data['PLANNAME']
            u = get_object_or_404(USER, USERNAME = 'Testuser')
            p = PLAN(PLANNAME=plan_name, CREATED_AT=timezone.now(), USERID=u)
            p.save()
            return HttpResponseRedirect(reverse('financial_planner:plan', args=(u.USERNAME, plan_name)))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CreatePlanForm()
    return render(request, 'financial_planner/index.html', {'form': form})


def plan(request, user_name, plan_name):
    user = get_object_or_404(USER, USERNAME = user_name)
    plan = get_object_or_404(PLAN, PLANNAME = plan_name, USERID = user.USERID)
    plan_name = plan.PLANNAME
    plan_id = plan.PLANID

    user_income_list = INCOMESOURCE.objects.filter(PLANID = plan_id )
    user_income_sum = user_income_list.aggregate(Sum('AMOUNT'))['AMOUNT__sum']
    context = {
        'plan_name': plan,
        'user_income_list': user_income_list,
        'user_name': user.USERNAME,
        'income_sum': user_income_sum,
        'plan_id': plan_id
    }
    return render(request, 'financial_planner/plan.html', context)

def add_source(request, user_name, plan_id):
    p = get_object_or_404(PLAN, PLANID = plan_id)
    if request.POST['category'] is None:
        i_s = INCOMESOURCE(SOURCENAME=request.POST['source'], AMOUNT=request.POST['amount'], PLANID=p)
    else:
        i_s = INCOMESOURCE(CATEGORY=request.POST['category'], SOURCENAME=request.POST['source'], AMOUNT=request.POST['amount'], PLANID=p)
    i_s.save()
    return HttpResponseRedirect(reverse('financial_planner:plan', args=(user_name, p.PLANNAME)))

def delete_source(request, user_name, plan_id, source_id):
    p = get_object_or_404(PLAN, PLANID = plan_id)
    instance = get_object_or_404(INCOMESOURCE, SOURCEID=source_id, PLANID=plan_id)
    instance.delete()
    return HttpResponseRedirect(reverse('financial_planner:plan', args=(user_name, p.PLANNAME)))
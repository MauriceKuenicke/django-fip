from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import INCOMESOURCE, USER, PLAN
from django.db.models import Sum




# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the financial_planner index.")


def plan(request, user_name, plan_id):
    user = get_object_or_404(USER, USERNAME = user_name).USERNAME
    plan = get_object_or_404(PLAN, PLANID = plan_id).PLANNAME


    user_income_list = INCOMESOURCE.objects.filter(PLANID = plan_id)
    user_income_sum = INCOMESOURCE.objects.aggregate(Sum('AMOUNT'))['AMOUNT__sum']
    plan = PLAN.objects.get(PLANID = plan_id).PLANNAME
    context = {
        'plan_name': plan,
        'user_income_list': user_income_list,
        'user_name': user,
        'income_sum': user_income_sum,
        'plan_id': plan_id
    }
    return render(request, 'financial_planner/plan.html', context)

def add_source(request, user_name, plan_id):
    p = get_object_or_404(PLAN, PLANID = plan_id)
    if request.POST['category'] is None:
        i_s = INCOMESOURCE(CATEGORY=request.POST['category'], SOURCENAME=request.POST['source'], AMOUNT=request.POST['amount'], PLANID=p)
    else:
        i_s = INCOMESOURCE(SOURCENAME=request.POST['source'], AMOUNT=request.POST['amount'], PLANID=p)
    i_s.save()
    return HttpResponseRedirect(reverse('financial_planner:plan', args=(user_name, plan_id)))

def delete_source(request, user_name, plan_id, source_id):
    instance = get_object_or_404(INCOMESOURCE, SOURCEID=source_id, PLANID=plan_id)
    instance.delete()
    return HttpResponseRedirect(reverse('financial_planner:plan', args=(user_name, plan_id)))
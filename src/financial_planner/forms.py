from django import forms

class CreatePlanForm(forms.Form):
    PLANNAME = forms.CharField(label='Plan Name', max_length=100)

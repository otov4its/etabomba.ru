# coding=utf8

from django.shortcuts import render_to_response, redirect
from forms import AccountCreationForm, AccountChangePasswordForm
from django.template import RequestContext

def password(request, template_name='password.djhtml'):
    "Set password page view"
    if request.method == 'POST':
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            form.save()
            cleaned_data = form.cleaned_data
            a_no = cleaned_data['acct']
            return redirect("/password/?success&a_no=%s" % (a_no, ))
    else:
        a_no = request.GET.get('a_no', '')
        form = AccountCreationForm(initial = {'acct': a_no})
        
    return render_to_response(template_name, {'form': form, 'success': request.GET.__contains__("success")}, context_instance=RequestContext(request))

def password_change(request, template_name='password_change.djhtml'):
    "Change password page view"
    if request.method == 'POST':
        form = AccountChangePasswordForm(request.POST)
        if form.is_valid():
            form.save()
            cleaned_data = form.cleaned_data
            a_no = cleaned_data['acct']
            return redirect("/password/change/?success&a_no=%s" % (a_no, ))
    else:
        a_no = request.GET.get('a_no', '')
        form = AccountChangePasswordForm(initial = {'acct': a_no})
            
    return render_to_response(template_name, {'form': form, 'success': request.GET.__contains__("success")}, context_instance=RequestContext(request))

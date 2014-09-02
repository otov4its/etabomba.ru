# coding=utf8

from django.shortcuts import render_to_response, get_object_or_404
from models import Paper
from etabomba.accounts.models import Account
from django.template import RequestContext
from etabomba.accounts.forms import PaymentStatusForm, AccountStatsForm
from forms import PaperSearchForm, TransactionApproveForm, PaperRegisterForm
from django.shortcuts import redirect
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import mail_admins
from etabomba.papers.helpers import get_stats

def home(request, template_name='home.djhtml'):
    """
    Home page view
    """
    if request.GET:
        form = PaperSearchForm(request.GET)
        form.full_clean() # Validate form for populate cleaned_data which use in templates
    else:
        form = PaperSearchForm()    
    
    stats = get_stats()
        
    return render_to_response(template_name, {'form': form, 'stats': stats}, context_instance=RequestContext(request))

def payment(request, p_no, template_name='payment.djhtml'):
    """
    Payment page view
    """
    p = get_object_or_404(Paper, no=p_no)
    
    paper_accts = ({p.acct1: p.acct_ok1}, {p.acct2: p.acct_ok2}, {p.acct3: p.acct_ok3}, {p.acct4: p.acct_ok4}, {p.acct5: p.acct_ok5}, {p.acct6: p.acct_ok6})
        
    
    payment_success = request.GET.get('payment_success', '') == 'True'
    whom = request.GET.get('whom', '')
                
    return render_to_response(template_name, {'paper_accts': paper_accts, 
                                              'p_no': p.no, 
                                              'payment_success': payment_success, 
                                              'whom': whom}, 
                              context_instance=RequestContext(request))

@csrf_exempt
def approve(request, template_name='approve.djhtml'):
    """
    Approve page view
    """
    if request.method == 'POST':
        mail_message = u"Купюра: %s\nОт: %s\nКому: %s\nСумма: %s\nIP сервера запроса: %s" % (request.POST.get('PAPER', ''), 
                                                                                            request.POST.get('PAYER_ACCOUNT', ''), 
                                                                                            request.POST.get('PAYEE_ACCOUNT', ''), 
                                                                                            request.POST.get('PAYMENT_AMOUNT', '0'), 
                                                                                            request.META['REMOTE_ADDR'])
        if float(request.POST.get('PAYMENT_AMOUNT', '0')) >= 1:
            data = {'p_no': request.POST.get('PAPER', ''),
                    'a_no_from': request.POST.get('PAYER_ACCOUNT', ''),
                    'a_no_to': request.POST.get('PAYEE_ACCOUNT', ''),
                    'password': 'xxx'}
            form = TransactionApproveForm(data)
            if form.is_valid():
                form.approve()
                mail_admins("Успешная транзакция", mail_message)
            else:
                mail_admins("Ошибка транзакции (валидация формы)", mail_message)
        else:
            mail_admins("Ошибка транзакции (сумма < 1)", mail_message)
    else:
        raise Http404
    
    return HttpResponse()

def register(request, template_name='register.djhtml'):
    """
    Register paper page view
    """
    if request.method == 'POST':
        form = PaperRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            cleaned_data = form.cleaned_data
            p_no = cleaned_data['p_no']
            a_no = cleaned_data['a_no']
            return redirect("/register/?success&p_no=%s&a_no=%s" % (p_no, a_no))
    else:
        a_no = request.GET.get('a_no', '')
        form = PaperRegisterForm(initial = {'a_no': a_no})
        
    return render_to_response(template_name, {'form': form, 'success': request.GET.__contains__("success")}, context_instance=RequestContext(request))

def faq(request, template_name='faq.djhtml'):
    """
    FAQ page view
    """
    return render_to_response(template_name, context_instance=RequestContext(request))

def about(request, template_name='about.djhtml'):
    """
    About page view
    """
    return render_to_response(template_name, context_instance=RequestContext(request))

def stats(request, template_name='stats.djhtml'):
    """
    Stats page view
    """
    a_no = None
    
    if request.GET.__contains__("a_no"):
        form = AccountStatsForm(request.GET)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            a_no = cleaned_data['a_no']
    else:
        form = AccountStatsForm()
    
    stats = get_stats(a_no)    
    
    return render_to_response(template_name, {'form': form, 'stats': stats}, context_instance=RequestContext(request))

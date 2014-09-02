# coding=utf8

from etabomba.accounts.models import Account
from etabomba.papers.models import Paper

def get_stats(account=''):
    """
    Get stats helper
    """
    
    p_count = Paper.objects.count()
    vip_count = Account.objects.filter(status="vip").count() + 5
    
    vip_accounts_top10 = Account.objects.filter(status="vip").order_by('-reg_papers_count')[:10]
    
    data = {'p_count': p_count, 'vip_count': vip_count, 'earned': vip_count*6, 'vip_accounts_top10': vip_accounts_top10}
    
    if account:
        account = Account.objects.get(acct=account)
        
        c1 = Paper.objects.filter(acct1=account.acct).count()
        c2 = Paper.objects.filter(acct2=account.acct).count()
        c3 = Paper.objects.filter(acct3=account.acct).count()
        c4 = Paper.objects.filter(acct4=account.acct).count()
        c5 = Paper.objects.filter(acct5=account.acct).count()
        c6 = Paper.objects.filter(acct6=account.acct).count()
        
        c_all = c1 + c2 + c3 + c4 + c5 + c6
        
        data.update({'account': account,
                     'c1': c1, 
                     'c2': c2, 
                     'c3': c3, 
                     'c4': c4, 
                     'c5': c5, 
                     'c6': c6, 
                     'c_all': c_all})
        
    return data 

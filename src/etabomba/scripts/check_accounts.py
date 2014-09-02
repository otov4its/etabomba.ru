# coding=utf8
# Stats
import header

from etabomba.papers.models import Paper
from etabomba.accounts.models import Account

def suspicious(acct):
    """
    Обнаружение подозрительных счетов, которые могут учавствовать в махинациях
    """
    if acct.reg_papers_count < 10000:
        c1 = Paper.objects.filter(acct1=acct.acct).count()
        c2 = Paper.objects.filter(acct2=acct.acct).count()
        c3 = Paper.objects.filter(acct3=acct.acct).count()
        c4 = Paper.objects.filter(acct4=acct.acct).count()
        c5 = Paper.objects.filter(acct5=acct.acct).count()
        c6 = Paper.objects.filter(acct6=acct.acct).count()
        c_all = c1 + c2 + c3 + c4 + c5 + c6
        
        if c2 > c1 or c3 > c1+c2 or c4 > c1+c2+c3 or c5 > c1+c2+c3+c4 or c6 > c1+c2+c3+c4+c5:
            return {acct.acct: {'c1': c1, 'c2': c2, 'c3': c3, 'c4': c4, 'c5': c5, 'c6': c6, 'c_all': c_all, 'reg_papers_count': acct.reg_papers_count}}
        
    return False

suspicious_accts_dic = {}
accts = Account.objects.all()

for acct in accts:
    s = suspicious(acct)
    if s:
        suspicious_accts_dic.update(s)
        
s = u"\n******* Подозрительных счетов: %s *******\n\n" % suspicious_accts_dic.__len__()
for k, v in suspicious_accts_dic.items():
    s += u"%s\t%s\n" % (k, v['reg_papers_count'])
    s += u"\tВ купюрах:\t%s\n" % v['c_all']
    s += u"\tНа 1 месте:\t%s\n" % v['c1']
    s += u"\tНа 2 месте:\t%s\n" % v['c2']
    s += u"\tНа 3 месте:\t%s\n" % v['c3']
    s += u"\tНа 4 месте:\t%s\n" % v['c4']
    s += u"\tНа 5 месте:\t%s\n" % v['c5']
    s += u"\tНа 6 месте:\t%s\n\n" % v['c6']
    
print s
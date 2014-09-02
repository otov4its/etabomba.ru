# coding=utf8
# Stats
import sys    
import header
from etabomba.papers.models import Paper
from etabomba.accounts.models import Account

arg_list = sys.argv[1:]

if arg_list[0] == 'all':
    acct_list = Account.objects.all()
else:
    acct_list = [Account.objects.get(acct=acct_no) for acct_no in arg_list]

for acct in acct_list:
    c1 = Paper.objects.filter(acct1=acct.acct).count()
    c2 = Paper.objects.filter(acct2=acct.acct).count()
    c3 = Paper.objects.filter(acct3=acct.acct).count()
    c4 = Paper.objects.filter(acct4=acct.acct).count()
    c5 = Paper.objects.filter(acct5=acct.acct).count()
    c6 = Paper.objects.filter(acct6=acct.acct).count()
    
    c_all = c1 + c2 + c3 + c4 + c5 + c6
    
    print "%s\t%s" % (acct.acct, acct.reg_papers_count)
    print "В купюрах, всего:\t%s" % c_all
    print "\tНа 1 месте:\t%s" % c1
    print "\tНа 2 месте:\t%s" % c2
    print "\tНа 3 месте:\t%s" % c3
    print "\tНа 4 месте:\t%s" % c4
    print "\tНа 5 месте:\t%s" % c5
    print "\tНа 6 месте:\t%s\n" % c6
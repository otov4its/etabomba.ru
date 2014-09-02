# coding=utf8
# Stats
import header

from etabomba.papers.models import Paper
from etabomba.accounts.models import Account

papers_count = Paper.objects.count()
accounts_count = Account.objects.count()
vip_accounts_count = Account.objects.filter(status="vip").count()
vip_accounts_top10 = Account.objects.filter(status="vip").order_by('-reg_papers_count')[:10]


print "Зарегистрировано купюр: %s" % papers_count
print "Cчетов в системе: %s из них со статусом vip: %s" % (accounts_count, vip_accounts_count)
print "Top 10 vip"
print "Счёт    Зарег.купюр"
for vip_account in vip_accounts_top10:
    print "%s    %s" % (vip_account.acct, vip_account.reg_papers_count)
from django.db import models
from django.contrib.auth.models import get_hexdigest

class Account(models.Model):
    "Account's model"
    acct = models.CharField(max_length=25, unique = True, help_text = "Account number")
    password = models.CharField(max_length=128, help_text = "Account password use '[algo]$[salt]$[hexdigest]'")
    status = models.CharField(max_length=25, blank = True, help_text = "Account status")
    acct1 = models.CharField(max_length=25, help_text = "#1 item accounts number list (it's equal Account.acct)")
    acct2 = models.CharField(max_length=25, help_text = "#2 item accounts number list")
    acct3 = models.CharField(max_length=25, help_text = "#3 item accounts number list")
    acct4 = models.CharField(max_length=25, help_text = "#4 item accounts number list")
    acct5 = models.CharField(max_length=25, help_text = "#5 item accounts number list")
    acct6 = models.CharField(max_length=25, help_text = "#6 item accounts number list")
    reg_date = models.DateTimeField(auto_now_add = True, help_text = "Account's registration date")
    ch_date = models.DateTimeField(auto_now = True, help_text = "Account's change date")
    reg_papers_count = models.PositiveIntegerField(default = 0, help_text = "Register papers count")
    
    def __unicode__(self):
        return u"""
        %s    %s    %s
        %s
        %s
        %s
        %s
        %s
        %s
        """ % (self.acct, self.status, self.reg_papers_count, self.acct1, self.acct2, self.acct3, self.acct4, self.acct5, self.acct6)
    
    def set_password(self, raw_password):
        import random
        algo = 'sha1'
        salt = get_hexdigest(algo, str(random.random()), str(random.random()))[:5]
        hsh = get_hexdigest(algo, salt, raw_password)
        self.password = '%s$%s$%s' % (algo, salt, hsh)
    
    def check_password(self, raw_password):
        """
        Returns a boolean of whether the raw_password was correct. Handles
        encryption formats behind the scenes.
        """
        algo, salt, hsh = self.password.split('$')
        return hsh == get_hexdigest(algo, salt, raw_password)
    
    def set_vip_status(self, p):
        """
        Set vip status to account and populate accounts list
        """
        self.status = "vip"
        self.acct1, self.acct2, self.acct3, self.acct4, self.acct5, self.acct6 = self.acct, p.acct2, p.acct3, p.acct4, p.acct5, p.acct6
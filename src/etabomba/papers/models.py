from django.db import models

class Paper(models.Model):
    "Paper's model"
    no = models.CharField(max_length = 25, unique = True, help_text = "Paper's number")
    acct1 = models.CharField(max_length = 25, help_text = "Paper's account number #1")
    acct2 = models.CharField(max_length = 25, help_text = "Paper's account number #2")
    acct3 = models.CharField(max_length = 25, help_text = "Paper's account number #3")
    acct4 = models.CharField(max_length = 25, help_text = "Paper's account number #4")
    acct5 = models.CharField(max_length = 25, help_text = "Paper's account number #5")
    acct6 = models.CharField(max_length = 25, help_text = "Paper's account number #6")
    acct_ok1 = models.CharField(max_length = 25, blank = True, help_text = "Paper's approve account number #1")
    acct_ok2 = models.CharField(max_length = 25, blank = True, help_text = "Paper's approve account number #2")
    acct_ok3 = models.CharField(max_length = 25, blank = True, help_text = "Paper's approve account number #3")
    acct_ok4 = models.CharField(max_length = 25, blank = True, help_text = "Paper's approve account number #4")
    acct_ok5 = models.CharField(max_length = 25, blank = True, help_text = "Paper's approve account number #5")
    acct_ok6 = models.CharField(max_length = 25, blank = True, help_text = "Paper's approve account number #6")
    hands = models.PositiveIntegerField(default = 1, help_text = "Hands count")
    reg_date = models.DateTimeField(auto_now_add = True, help_text = "Paper's registration date")
    ch_date = models.DateTimeField(auto_now = True, help_text = "Paper's change date")
    
    def __unicode__(self):        
        return u"""
        %s
        %s    %s
        %s    %s
        %s    %s
        %s    %s
        %s    %s
        %s    %s
        %s
        """ % (self.no, self.acct1, self.acct_ok1, self.acct2, self.acct_ok2, self.acct3, self.acct_ok3, self.acct4, self.acct_ok4, self.acct5, self.acct_ok5, self.acct6, self.acct_ok6, self.hands,)
    
    def get_acct_n(self, a_no_to):
        """
        Get ordering number in paper's accounts list by PM account
        
        Raises ValueError if the account is not present in paper's account list
         
        return integer 
        """
        accts_list = [self.acct1, self.acct2, self.acct3, self.acct4, self.acct5, self.acct6]
        
        i = accts_list.index(a_no_to)
        
        return i + 1
    
    def is_time_to_shift(self):
        """
        Checks if time to make the shift
        
        return bool
        """
        return self.acct_ok1 != "" and self.acct_ok1 == self.acct_ok2 == self.acct_ok3 == self.acct_ok4 == self.acct_ok5 == self.acct_ok6
    
    def shift(self):
        """
        Shift accounts, reset approve accounts and +1 hands count
        """ 
        li = [self.acct1, self.acct2, self.acct3, self.acct4, self.acct5, self.acct6]
        del li[5]
        li.insert(0, self.acct_ok1)
        self.acct1, self.acct2, self.acct3, self.acct4, self.acct5, self.acct6 = li
        
        self.acct_ok1 = self.acct_ok2 = self.acct_ok3 = self.acct_ok4 = self.acct_ok5 = self.acct_ok6 = ''
        
        self.hands += 1
        
        
        
        
        
            
        
        
        
        
        
        
        
# coding=utf8

from django import forms
from models import Paper
from etabomba.accounts.models import Account

class PaperSearchForm(forms.Form):
    """
    A paper search form
    """
    p_no = forms.RegexField(label="Номер купюры", max_length=25, regex=u'^[A-Za-zА-Яа-яЁё0-9\s]{1,25}$', 
                            error_messages = {'invalid': "Только буквы и цифры",
                                              'required': "Это обязательное поле"}, 
                            widget=forms.TextInput(attrs={'required':'required', 'autofocus': 'autofocus'}),
                            help_text="Введите номер купюры, буквы и цифры без пробелов, регистр букв имеет значение (например аУ1414808)")
    
    def clean_p_no(self):
        p_no = self.cleaned_data["p_no"].replace(' ', '')
        
        if not Paper.objects.filter(no=p_no).exists():
            raise forms.ValidationError("Купюра не зарегистрирована в системе")
        
        return p_no

class TransactionApproveForm(forms.Form):
    """
    A transaction approve form
    """
    p_no = forms.RegexField(label="Номер купюры", max_length=25, regex=u'^[A-Za-zА-Яа-яЁё0-9]{1,25}$', 
                            error_messages = {'invalid': "Только буквы и цифры без пробелов",
                                              'required': "Это обязательное поле"}, 
                            widget=forms.TextInput(attrs={'required':'required', 'autofocus': 'autofocus'}),
                            help_text="Номер купюры, буквы и цифры без пробелов, регистр букв имеет значение (например аУ1414808)")
    a_no_from = forms.RegexField(label="Номер счёта PM с которого поступил платёж", max_length=8, regex=r'^U[0-9]{7}$', 
                                 error_messages = {'invalid': "Номер счёта должен быть в формате U1234567", 
                                                   'required': "Это обязательное поле"},
                                 widget=forms.TextInput(attrs={'required':'required'}), 
                                 help_text="Номер счёта PM с которого поступил платёж (например U1234567)")
    a_no_to = forms.RegexField(label="Ваш номер счёта PM", max_length=8, regex=r'^U[0-9]{7}$', 
                               error_messages = {'invalid': "Номер счёта должен быть в формате U1234567", 
                                                 'required': "Это обязательное поле"},
                               widget=forms.TextInput(attrs={'required':'required'}),
                               help_text="Ваш номер счёта PM (например U1234567)")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(render_value=False, attrs={'required':'required'}),
                               error_messages = {'required': "Это обязательное поле"},
                               help_text="Пароль на сайте")
    
    __p = None
    
    __a = None
    
    def clean_p_no(self):
        p_no = self.cleaned_data["p_no"]
        
        try:
            p = Paper.objects.get(no=p_no)
        except Paper.DoesNotExist:
            raise forms.ValidationError("Купюра не зарегистрированна в системе")
        
        self.__p = p
        
        return p_no
    
    def clean_password(self):
        a_no_to = self.cleaned_data.get("a_no_to", "")
        password = self.cleaned_data["password"]
        
        try:
            a = Account.objects.get(acct=a_no_to)
        except Account.DoesNotExist:
            raise forms.ValidationError("Неверное сочетание номера счёта и пароля")
        #if not a.check_password(password):
        #    raise forms.ValidationError("Неверное сочетание номера счёта и пароля")
        
        self.__a = a

        return password
    
    def clean(self):
        cleaned_data = self.cleaned_data
        p_no = cleaned_data.get("p_no")
        a_no_from = cleaned_data.get("a_no_from")
        a_no_to = cleaned_data.get("a_no_to")
        password = cleaned_data.get("password")

        if p_no and a_no_from and a_no_to and password:
            # Only do something if all fields are valid so far.
            try:
                n = self.__p.get_acct_n(a_no_to)
            except ValueError:
                raise forms.ValidationError("Вы не можете подтвердить транзакцию, ваш номер счёта отсутствует в списке счетов купюры")
            
            if getattr(self.__p, "acct_ok%s" % n):
                raise forms.ValidationError("Транзакция уже подтверждена")
            
            try:
                n = self.__p.get_acct_n(a_no_from)
            except ValueError:
                pass
            else:
                raise forms.ValidationError("Вы не можете подтвердить транзакцию, т.к. номер счёта отправителя есть в списке счетов купюры")
            
        # Always return the full collection of cleaned data.
        return cleaned_data
    
    def approve(self):
        """
        Approve transaction
        """
        a_no_from = self.cleaned_data.get("a_no_from")
                        
        n = self.__p.get_acct_n(self.__a.acct)
        setattr(self.__p, "acct_ok%s" % n, a_no_from)
        
        if self.__p.is_time_to_shift():
            # It's time to shift
            self.__p.shift()
            a, created = Account.objects.get_or_create(acct=a_no_from)
            # Set vip status only once for account
            if a.status != "vip":
                a.set_vip_status(self.__p)
                a.save()
                
        self.__p.save()
        
    
class PaperRegisterForm(forms.Form):
    """
    Paper register form
    """
    #TODO: Make a multi papers creation for one time
    #TODO: Captchas for all forms may be
    p_no = forms.RegexField(label="Номер купюры", max_length=25, regex=u'^[A-Za-zА-Яа-яЁё0-9]{1,25}$', 
                            error_messages = {'invalid': "Только буквы и цифры без пробелов",
                                              'required': "Это обязательное поле"},
                            widget=forms.TextInput(attrs={'required': 'required', 'autofocus': 'autofocus'}),
                            help_text="Номер купюры, буквы и цифры без пробелов, регистр букв имеет значение (например аУ1414808)")
    a_no = forms.RegexField(label="Номер счёта PM", max_length=8, regex=r'^U[0-9]{7}$', 
                            error_messages = {'invalid': "Номер счёта должен быть в формате U1234567",
                                              'required': "Это обязательное поле"},
                            widget=forms.TextInput(attrs={'required': 'required'}),
                            help_text="Ваш номер счёта PM (например U1234567)")
    
    __a = None
    
    def clean_p_no(self):
        p_no = self.cleaned_data["p_no"]
        
        if Paper.objects.filter(no=p_no).exists():
            raise forms.ValidationError("Купюра уже зарегистрирована в системе")
        
        return p_no
    
    def clean_a_no(self):
        a_no = self.cleaned_data["a_no"]
        
        if self.cleaned_data.get("p_no"):
            try:
                a = Account.objects.get(acct=a_no)
            except Account.DoesNotExist:
                raise forms.ValidationError("Счёт отсутствует в системе")
            
            if a.status != "vip":
                raise forms.ValidationError("Только счета со статусом 'vip' могут регистрировать купюры в системе")
            
            self.__a = a
        
        return a_no
    
    def save(self):
        """
        Save registered paper to database
        """
        p_no = self.cleaned_data["p_no"]
        Paper.objects.create(no=p_no, 
                             acct1=self.__a.acct1, 
                             acct2=self.__a.acct2, 
                             acct3=self.__a.acct3, 
                             acct4=self.__a.acct4, 
                             acct5=self.__a.acct5, 
                             acct6=self.__a.acct6)
        
        self.__a.reg_papers_count += 1
        self.__a.save()
        
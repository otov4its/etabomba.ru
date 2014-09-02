# coding=utf8

from django import forms
from models import Account

class AccountCreationForm(forms.ModelForm):
    """
    A form that creates a account from the given account number and password.
    """
    acct = forms.RegexField(label="Номер счёта PM", max_length=8, regex=r'^U[0-9]{7}$', 
                            error_messages = {'invalid': "Номер счёта должен быть в формате U1234567", 
                                              'required': "Это обязательное поле"},
                            widget=forms.TextInput(attrs={'required':'required', 'autofocus': 'autofocus'}),
                            help_text = "Ваш номер счёта PM, например U1234567")
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(render_value=False, attrs={'required':'required'}),
                                error_messages = {'required': "Это обязательное поле"},
                                help_text = "Пароль на сайте")
    password2 = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput(render_value=False, attrs={'required':'required'}), 
                                error_messages = {'required': "Это обязательное поле"},
                                help_text = "Повторите пароль")
    accept = forms.BooleanField(label="Я ознакомлен с предупреждением",
                                error_messages = {'required': "Это обязательное поле"},
                                widget=forms.CheckboxInput(attrs={'required':'required'}))

    class Meta:
        model = Account
        fields = ("acct",)

    def clean_acct(self):
        acct = self.cleaned_data["acct"]
        
        if Account.objects.filter(acct=acct).exists():
            raise forms.ValidationError("Номер счёта уже зарегистрирован в системе")
        
        return acct
        
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError("Не совпадает пароль")
        return password2

    def save(self, commit=True):
        acct = super(AccountCreationForm, self).save(commit=False)
        acct.set_password(self.cleaned_data["password1"])
        if commit:
            acct.save()
        return acct

class AccountChangePasswordForm(forms.Form):
    """
    A form that change a account password
    """
    acct = forms.RegexField(label="Номер счёта PM", max_length=8, regex=r'^U[0-9]{7}$', 
                            error_messages = {'invalid': "Номер счёта должен быть в формате U1234567", 
                                              'required': "Это обязательное поле"},
                            widget=forms.TextInput(attrs={'required':'required', 'autofocus': 'autofocus'}),
                            help_text = "Ваш номер счёта PM, например U1234567")
    old_password = forms.CharField(label="Старый пароль", widget=forms.PasswordInput(render_value=False, attrs={'required':'required'}),
                                error_messages = {'required': "Это обязательное поле"},
                                help_text = "Старый пароль на сайте")
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(render_value=False, attrs={'required':'required'}),
                                error_messages = {'required': "Это обязательное поле"},
                                help_text = "Новый пароль на сайте")
    password2 = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput(render_value=False, attrs={'required':'required'}), 
                                error_messages = {'required': "Это обязательное поле"},
                                help_text = "Повторите новый пароль")
    
    __a = None
    
    def clean_old_password(self):
        acct = self.cleaned_data.get("acct", "")
        old_password = self.cleaned_data["old_password"]
        
        try:
            a = Account.objects.get(acct=acct)
        except Account.DoesNotExist:
            raise forms.ValidationError("Неверное сочетание номера счёта и пароля")
        
        if not a.check_password(old_password):
            raise forms.ValidationError("Неверное сочетание номера счёта и пароля")
        
        self.__a = a
        
        return old_password
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError("Не совпадает пароль")
        return password2
    
    def save(self):
        password2 = self.cleaned_data["password2"]
        self.__a.set_password(password2)
        self.__a.save()
    
class PaymentStatusForm(forms.Form):
    """
    A payment status form
    """
    a_no = forms.RegexField(label="PM", max_length=8, regex=r'^U[0-9]{7}$', 
                            error_messages = {'invalid': "Номер счёта должен быть в формате U1234567", 
                                              'required': "Это обязательное поле"}, 
                            widget=forms.TextInput(attrs={'required':'required', 'autofocus': 'autofocus'}),
                            help_text="Ваш номер счёта PM, например U1234567")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(render_value=False, attrs={'required':'required'}),
                               error_messages = {'required': "Это обязательное поле"}, 
                               help_text="Пароль на сайте")
    
    def clean_password(self):
        a_no = self.cleaned_data.get("a_no", "")
        password = self.cleaned_data["password"]
        try:
            a = Account.objects.get(acct=a_no)
        except Account.DoesNotExist:
            raise forms.ValidationError("Неверное сочетание номера счёта и пароля")
        if not a.check_password(password):
            raise forms.ValidationError("Неверное сочетание номера счёта и пароля")
        return password

class AccountStatsForm(forms.Form):
    """
    Account status form
    """
    a_no = forms.RegexField(label="PM", max_length=8, regex=r'^U[0-9]{7}$', 
                            error_messages = {'invalid': "Номер счёта должен быть в формате U1234567", 
                                              'required': "Это обязательное поле"}, 
                            widget=forms.TextInput(attrs={'required':'required', 'autofocus': 'autofocus'}),
                            help_text="Ваш номер счёта PM, например U1234567")
    
    def clean_a_no(self):
        a_no = self.cleaned_data["a_no"]
        
        if not Account.objects.filter(acct=a_no).exists():
            raise forms.ValidationError("Счёт не найден в системе")
        
        return a_no
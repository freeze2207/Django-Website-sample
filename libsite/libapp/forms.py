from django import forms
from libapp.models import Suggestion
from libapp.models import Libuser

class SuggestionForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        exclude = ['num_interested']
        fields=['title','pubyr','type','cost','comments']
        widgets={type:forms.RadioSelect}

    # title = forms.CharField(widget=forms.TextInput(attrs={'required':True, 'max_length': 100, 'class': 'form-control'}))
    # pubyr = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    # type = forms.RadioSelect()
    # cost = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}),label='Estimated cost in Dollars')
    # comments = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))


class SearchlibForm(forms.Form):
    title = forms.CharField(max_length=100, required=False)
    by = forms.CharField(max_length=100, required=False)



class loginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))


class UserForm(forms.ModelForm):
    class Meta:
        model=Libuser
        fields=['username','first_name','last_name','email','phone','password']
        widgets = {'password' : forms.PasswordInput()}

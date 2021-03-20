from django import forms
class NameForm(forms.Form):
    roomname=forms.CharField(max_length=250)
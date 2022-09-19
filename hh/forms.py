from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'Заголовок сообщения', 'class': 'form-control'}), max_length=100)
    email = forms.EmailField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'email', 'class': 'form-select'}), max_length=100)
    message = forms.CharField(label='', widget=forms.Textarea(
        attrs={'placeholder': 'Сообщение', 'class': 'form-control'}), max_length=300)

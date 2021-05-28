from django import forms


class StudentForm(forms.Form):
    firstname = forms.CharField(label="Enter first name", max_length=50)
    lastname = forms.CharField(label="Enter last name", max_length=10)
    email = forms.EmailField(label="Enter Email")
    file_filed = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

from django import forms
from .models import Task

#formulario personalizado proveniente de models (DB) y que se pueden indicar los campos necesarios en la clase Meta con el diccionario field
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title','description', 'important']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'write a title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'write a description'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input text-center'}),
        }
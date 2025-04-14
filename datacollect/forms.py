from django import forms


class ImportCSVForm(forms.Form):
    csvfile = forms.FileField(label="csv-file")

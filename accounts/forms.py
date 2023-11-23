from django import forms

class StockInputForm(forms.Form):
    codes = forms.CharField(
        label='Enter stock codes (comma-separated)',
        widget=forms.TextInput(attrs={'placeholder': 'e.g., 005930,005380'}),
    )
    names = forms.CharField(
        label='Enter stock names (comma-separated)',
        widget=forms.TextInput(attrs={'placeholder': 'e.g., 삼성전자,현대자동차'}),
    )
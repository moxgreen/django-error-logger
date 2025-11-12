from django import forms

class TestPostErrorForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        initial='testuser',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        initial='secret123',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text='This field will be redacted in logs'
    )
    email = forms.EmailField(
        initial='test@example.com',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    token = forms.CharField(
        max_length=200,
        initial='abc123token',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text='This field will be redacted in logs'
    )

class TestLargePostForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        initial='testuser',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        initial='secret123',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text='This field will be redacted in logs'
    )
    large_field = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 10,
            'placeholder': 'This will be filled with 150KB of data automatically'
        }),
        required=False,
        initial='x' * (150 * 1024)  # 150KB of data
    )
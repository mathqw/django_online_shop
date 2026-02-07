from django import forms
from .models import Card

class CardForm(forms.ModelForm):
    card_number = forms.CharField(
        max_length=16,
        min_length=16,
        label="Номер картки",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Card
        fields = ['card_name', 'card_type']

        widgets = {
            'card_name': forms.TextInput(attrs={'class': 'form-control'}),
            'card_type': forms.Select(attrs={'class': 'form-select'}),
        }

    def save(self, commit=True, user=None):
        card = super().save(commit=False)

        number = self.cleaned_data['card_number']
        card.last4 = number[-4:]

        if user:
            card.user = user

        if commit:
            card.save()

        return card
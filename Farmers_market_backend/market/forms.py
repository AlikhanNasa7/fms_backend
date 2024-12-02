from django import forms

class FarmerRejectionForm(forms.Form):
    rejection_reason = forms.CharField(widget=forms.Textarea, label="Rejection Reason", required=True)

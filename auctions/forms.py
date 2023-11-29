from django import forms


class NewListingForm(forms.Form):
    title = forms.CharField(label='Title:', max_length=100, required=True, 
                            widget=forms.TextInput(attrs={'class': 'form-control w-50'}))
    img_url = forms.URLField(label='Image URL:', max_length=100, required=True, 
                            widget=forms.TextInput(attrs={'class': 'form-control w-50'}))
    category = forms.CharField(label='Category:', max_length=100, required=True, 
                            widget=forms.TextInput(attrs={'class': 'form-control w-50'}))
    starting_bid = forms.FloatField(label='Starting bid', min_value=0,
                            widget=forms.TextInput(attrs={'class': 'form-control w-50'}))
    description = forms.CharField(label='description:', required=True, 
                            widget=forms.Textarea(attrs={'class': 'form-control w-50'}))


class NewBidForm(forms.Form):
    price = forms.DecimalField(
        min_value=0, 
        decimal_places=2,
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control w-50', "placeholder": "Bid"}))
from django import forms


##################################################################
class formAdvisor (forms.Form):
    advisorCode = forms.CharField(max_length=5)
    firstName   = forms.CharField(max_length=40)
    lastName    = forms.CharField(max_length=40)
    BranchCode  = forms.CharField(max_length=5)
    LangCode    = forms.CharField(max_length=1)
    eMail       = forms.CharField(max_length=100)

    def clean_data  (self):
        cleaned_data = super ( formAdvisor, self ).clean ()
        advisorCode = cleaned_data.get('advisorCode')
        BranchCode = cleaned_data.get('BranchCode')
        LangCode = cleaned_data.get('LangCode')
        eMail = cleaned_data.get('eMail')

##################################################################
class formDemographic  (forms.Form):
    advisorCode = forms.CharField(max_length=5)
    BranchCode  = forms.CharField(max_length=5)
    LangCode    = forms.CharField(max_length=1)

    def clean_data  (self):
        cleaned_data = super ( formAdvisor, self ).clean ()
        advisorCode = cleaned_data.get('advisorCode')

##################################################################

from django import forms
from kpbt.centers.models import BowlingCenter, CenterAddress

class CreateBowlingCenterForm(forms.ModelForm):
	class Meta:
		model= BowlingCenter
		exclude = ['manager']
		fields=('name', 'num_lanes')
		
class CreateCenterAddressForm(forms.ModelForm):
	class Meta:
		model = CenterAddress
		exclude = ['bowling_center']
		fields = ('__all__')
		
		
class UpdateCenterForm(forms.ModelForm):
	#center_name = forms.CharField(max_length=32)
	#num_lanes = forms.IntegerField(min_value=2, label='Number of lanes')
	
	class Meta:
		model = BowlingCenter
		exclude = ['manager']
		fields = ('__all__')
	
		
class UpdateAddressForm(forms.ModelForm):
	class Meta:
		model = CenterAddress
		exclude = ['bowling_center']
		fields = ('__all__')

class UpdateManagerForm(forms.ModelForm):
	class Meta:
		model = BowlingCenter
		fields =('manager',)
		
class DeleteLeagueForm(forms.Form):
	delete_confirmation = forms.CharField(max_length=6)
	
	def clean(self):
		cleaned_data=super().clean()
		
		confirmation = cleaned_data.get("delete_confirmation")
		
		if confirmation:
			if confirmation != "DELETE":
				raise forms.ValidationError(
					"Please enter DELETE to confirm league deletion."
				)
	
"""		
class CenterSelectForm(forms.modelForm):
	class Meta:
		model = BowlingCenter
		fields = ('name')
"""
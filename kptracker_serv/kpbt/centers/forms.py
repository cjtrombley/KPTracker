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
"""		
class CenterSelectForm(forms.modelForm):
	class Meta:
		model = BowlingCenter
		fields = ('name')
"""
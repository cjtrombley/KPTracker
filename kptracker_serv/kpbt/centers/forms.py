from django import forms
from kpbt.centers.models import BowlingCenter

class BowlingCenterForm(forms.ModelForm):
	class Meta:
		model= BowlingCenter
		fields=('name', 'num_lanes', 'manager')

"""		
class CenterSelectForm(forms.modelForm):
	class Meta:
		model = BowlingCenter
		fields = ('name')
"""
from django import forms
from kpbt.bowling_centers.models import BowlingCenter

class BowlingCenterForm(forms.ModelForm):
	class Meta:
		model= BowlingCenter
		fields=('center_name', 'num_lanes')
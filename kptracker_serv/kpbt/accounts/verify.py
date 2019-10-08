# This would be called whenever someone goes to this url 
#re_path(r'verify/(.*)', include('kpbt.accounts.verify')),

#It would make a request to the mysql server to check if the account existed ... etc
def verify(request, token):
	print("Request:", request)
	print("Token:", token)
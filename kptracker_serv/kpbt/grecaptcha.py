import requests

# captchaSuccess = checkGReCaptchaResponse(args["g-recaptcha-response"], self.request.remote_ip, grecaptchaSecretKey)
																		# This is how it is done in cyclone. Needs updating for django
def checkGReCaptchaResponse(clientResponse, remoteip, secret):
	data = {
		"secret": secret,
		"response": clientResponse,
		"remoteip": remoteip
	}
	r = requests.post("https://www.google.com/recaptcha/api/siteverify", data=data)
	return json.loads(r.text)["success"]
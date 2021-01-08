import requests
import smtplib
import os
import config
from email.message import EmailMessage

def perform_search(dept, num, addr):
	cookies = {
    	'DCA0_reg809': '^!YPG3FDol20xyoTDfoHF0Eo0+q6dMPe55HMAtrnN0fTInIXN3dKBuy0R0Ur4EKXTuJNYnEYbwkgRx3es=',
	}

	headers = {
	    'Connection': 'keep-alive',
	    'Cache-Control': 'max-age=0',
	    'Upgrade-Insecure-Requests': '1',
	    'Origin': 'https://www.reg.uci.edu',
	    'Content-Type': 'application/x-www-form-urlencoded',
	    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
	    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
	    'Sec-Fetch-Site': 'same-origin',
	    'Sec-Fetch-Mode': 'navigate',
	    'Sec-Fetch-User': '?1',
	    'Sec-Fetch-Dest': 'document',
	    'Referer': 'https://www.reg.uci.edu/perl/WebSoc',
	    'Accept-Language': 'en-US,en;q=0.9',
	}

	data = {
	  'Submit': 'Display Text Results',
	  'YearTerm': '2021-03',
	  'ShowComments': 'on',
	  'ShowFinals': 'on',
	  'Breadth': 'ANY',
	  'Dept': dept,
	  'CourseNum': num,
	  'Division': 'ANY',
	  'CourseCodes': '',
	  'InstrName': '',
	  'CourseTitle': '',
	  'ClassType': 'ALL',
	  'Units': '',
	  'Days': '',
	  'StartTime': '',
	  'EndTime': '',
	  'MaxCap': '',
	  'FullCourses': 'ANY',
	  'FontSize': '100',
	  'CancelledCourses': 'Exclude',
	  'Bldg': '',
	  'Room': ''
	}

	response = requests.post(addr, headers=headers, cookies=cookies, data=data)
	return response.text

#def send_email

if __name__ == "__main__":

	class_department = config.class_department
	class_number = config.class_number
	sections = config.sections
	url = config.url
	email_address = config.email_address

	text = ('    ' + perform_search(class_department, class_number, url).split('Rstr Status')[1].strip()).split('\n')
	if not os.path.exists("output.txt"):
		open("output.txt", 'w').close()
	with open("output.txt", 'r+') as outfile:
		old = []
		new = []
		counter = 0
		
		for x in text: # add text from website to new
			if len(x) > 50 and x[14] in sections: # get section number/letter
				counter += 1
				new.append(x[14] + ": " + x[122:126]) # ex. A: OPEN		
		if os.path.getsize("output.txt") > 0: # if output.txt is not empty
			for num, x in enumerate(outfile): # add text from output.txt to old
				old.append(x.strip())
				if not x.strip() == new[num]:
					print("cool")
					#send email w/ message ("Class has changed status.\n\n" + new[num])
			# compare old and new, email meader@uci.edu if there is a difference
		if not old == new:
			outfile.seek(0)
			for x in new:
				outfile.write(x + "\n")
		
		print(old)
		print(new)

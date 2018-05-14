import shodan
import mechanize
import sys
import urllib
import re
import math
import getpass

SHODAN_API_KEY = "sRrsvRIMHSDBHeqAnARdfnFB668LDR9Y" #input you SHODAN_API_KEY here
#use 2 global variables to represent two most recent found ip, in order to avoid dupliacated ips 
c_ip = None
prv_ip = None

def print_ip(text):
	global c_ip
	global prv_ip
	for line in text.splitlines():
		ip =re.findall( r'[0-9]+(?:\.[0-9]+){3}', line )
		if ip:
			prv_ip = c_ip
			c_ip = ip[0]
			if prv_ip != c_ip:
				print ip[0]


if len(sys.argv) != 2:
	print "Usage: python " + sys.argv[0] + " <your_query>" 
	sys.exit(0)
else:
	api = shodan.Shodan(SHODAN_API_KEY)
	n_result = api.count(sys.argv[1])
	print "number of results: " + str(n_result['total'])

	equery=urllib.quote_plus(sys.argv[1]) #encode query
br = mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = [("User-agent","Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13")]

sign_in = br.open("https://account.shodan.io/login")
br.select_form(nr = 0) 

br["username"] = raw_input("username:")
br["password"] = getpass.getpass(prompt='password:')
logged_in = br.submit()
if logged_in.code != 200:
	print "[!] Login error, Program exit..."
	sys.exit(0)

else:
	qurl = "https://www.shodan.io/search?query=" + equery
	res = br.open(qurl)
	if res.code!=200:
		print "failed at query: " + qurl  
		sys.exit(0)
	else:
		print_ip(str(res.read()))


	#remaining pages, note each page has 10 result, and there are n_result['total'] in total
	max_npages = math.ceil(n_result['total']/10)
	#print type(max_npages)
	for p in range(2, int(max_npages)+1):
		qurl = "https://www.shodan.io/search?query=" + equery + "&page=" + str(p)
		res = br.open(qurl)
		if res.code!=200:
			print "failed at query: " + qurl  
			sys.exit(0)
		else:
			print_ip(str(res.read()))
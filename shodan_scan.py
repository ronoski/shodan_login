import shodan
import mechanize
import sys
import urllib
import re
import math
import getpass

SHODAN_API_KEY = "sRrsvRIMHSDBHeqAnARdfnFB668LDR9Y" #input you SHODAN_API_KEY here

# Windows Server 2008 R2 Enterprise 7601 Service Pack 1
# Windows Server 2008 R2 Standard 7601 Service Pack 1
# Windows Server 2008 R2 Datacenter 7601 Service Pack 1
# Windows Server 2008 R2 Foundation 7601 Service Pack 1
# Windows Server 2008 R2 Standard 7600

# Windows Server 2012 R2 Standard 9600
# Windows Server 2012 R2 Datacenter 9600
# Windows Server 2012 Standard 9200
# Windows Server 2012 R2 Standard Evaluation 9600
# Windows Server 2012 Datacenter 9200
# Windows server 2016
# Windows 10

c_ip = None
prv_ip = None
file_index = 0
ip_count = 0
#countries = ['AF','AL','DZ','AS','AD','AO','AI','AQ','AG','AR','AM','AW','AU','AT','AZ','BS','BH','BD','BB','BY','BE','BZ','BJ','BM','BT','BO','BA','BW','BV','BR','IO','BN','BG','BF','BI','KH','CM','CA','CV','KY','CF','TD','CL','CN','CX','CC','CO','KM','CG','CD','CK','CR','CI','HR','CU','CY','CZ','DK','DJ','DM','DO','EC','EG','SV','GQ','ER','EE','ET','FK','FO','FJ','FI','FR','GF','PF','TF','GA','GM','GE','DE','GH','GI','GR','GL','GD','GP','GU','GT','GN','GW','GY','HT','HM','HN','HK','HU','IS','IN','ID','IR','IQ','IE','IL','IT','JM','JP','JO','KZ','KE','KI','KP','KR','KW','KG','LA','LV','LB','LS','LR','LY','LI','LT','LU','MO','MK','MG','MW','MY','MV','ML','MT','MH','MQ','MR','MU','YT','MX','FM','MD','MC','MN','MS','MA','MZ','MM','NA','NR','NP','NL','AN','NC','NZ','NI','NE','NG','NU','NF','MP','NO','OM','PK','PW','PS','PA','PG','PY','PE','PH','PN','PL','PT','PR','QA','RE','RO','RU','RW','SH','KN','LC','PM','VC','WS','SM','ST','SA','SN','CS','SC','SL','SG','SK','SI','SB','SO','ZA','GS','ES','LK','SD','SR','SJ','SZ','SE','CH','SY','TW','TJ','TZ','TH','TL','TG','TK','TO','TT','TN','TR','TM','TC','TV','UG','UA','AE','GB','US','UM','UY','UZ','VU','VN','VG','VI','WF','EH','YE','ZW']
countries = ['AF','AL','DZ','AS','AD','AO','AI','AQ','AG','AR','AM','AW','AU','AT','AZ','BS','BH','BD','BB','BY','BE','BZ','BJ','BM','BT','BO','BA','BW','BV','BR','IO','BN','BG','BF','BI','KH','CM','CA','CV','KY','CF','TD','CL','CN','CX','CC','CO','KM','CG','CD','CK','CR','CI','HR','CU','CY','CZ','DK','DJ','DM','DO','EC','EG','SV','GQ','ER','EE','ET','FK','FO','FJ','FI','FR','GF','PF','TF','GA','GM','GE','DE','GH','GI','GR','GL','GD','GP','GU','GT','GN','GW','GY','HT','HM','HN','HK','HU','IS','IN','ID','IR','IQ','IE','IL','IT','JM','JP','JO','KZ','KE','KI','KP','KR','KW','KG','LA','LV','LB','LS','LR','LY','LI','LT','LU','MO','MK','MG','MW','MY','MV','ML','MT','MH','MQ','MR','MU','YT','MX','FM','MD','MC','MN','MS','MA','MZ','MM','NA','NR','NP','NL','AN','NC','NZ','NI','NE','NG','NU','NF','MP','NO','OM','PK','PW','PS','PA','PG','PY','PE','PH','PN','PL','PT','PR','QA','RE','RO','RU','RW','SH','KN','LC','PM','VC','WS','SM','ST','SA','SN','CS','SC','SL','SG','SK','SI','SB','SO','ZA','GS','ES','LK','SD','SR','SJ','SZ','SE','CH','SY','TW','TJ','TZ','TH','TL','TG','TK','TO','TT','TN','TR','TM','TC','TV','UG','UA','AE','GB','US','UM','UY','UZ','VU','VN','VG','VI','WF','EH','YE','ZW']
excluded_countries = ['BR','CL','CN','ES','GR','HK','ID','IN','IR','IT','JP','KR','KZ','MX','MY','LA','KH','PK','AF','RU','SA','TH','TW','UA','VN']
def print_ip(text):
	global c_ip
	global prv_ip
	global ip_count
	global file_index
	filename = sys.argv[2] + "_00" +str(file_index)
	f = open(filename, 'a')

	for line in text.splitlines():
		ip =re.findall( r'[0-9]+(?:\.[0-9]+){3}', line )
		if ip:
			ip_count = ip_count + 1
			if ip_count > 3000:
				ip_count =0
				file_index = file_index +1 
			prv_ip = c_ip
			c_ip = ip[0]
			if prv_ip != c_ip:
				print ip[0]
				f.write('\n'+ip[0])
	f.close()


if len(sys.argv) != 3:
	print "Usage: python " + sys.argv[0] + " <your_query>" 
	sys.exit(0)
else:
	api = shodan.Shodan(SHODAN_API_KEY)
	
def do_querry(br, user_query):
	n_result = api.count(user_query)
	print "[+]number of results: " + str(n_result['total'])
	if n_result == 0:
		return
	equery=urllib.quote_plus(user_query) #encode query
	#First page
	qurl = "https://www.shodan.io/search?query=" + equery
	res = br.open(qurl,timeout=300.0)
	if res.code!=200:
		print "[!]failed at query: " + qurl  
		return
	else:
		print_ip(str(res.read()))

	#remaining pages, note each page has 10 result, and there are n_result['total'] in total
	max_npages = math.ceil(n_result['total']/10)
	#print type(max_npages)
	max_npages = 200 if max_npages > 200 else max_npages  #shodan limit max_page = 200
	for p in range(2, int(max_npages)+1):
		qurl = "https://www.shodan.io/search?query=" + equery + "&page=" + str(p)
		res = br.open(qurl, timeout=300.0)
		if res.code!=200:
			print "[!]failed at query: " + qurl  
			return
		else:
			print_ip(str(res.read()))
	return


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
	print "[+]Shodan login success"
	for country in countries:
		if country not in excluded_countries:
			print "[+]scan country: " + country
			user_query = sys.argv[1] + " country:" + "\'" + country + "\'"
			do_querry(br,user_query )
	

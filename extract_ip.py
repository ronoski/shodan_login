import re
import sys

f_x64 = open('x64.txt','a')
f_x86 = open('x86.txt','a')
f_unknown = open('unknown.txt','a')
f_all = open('all.txt','a')
with open(sys.argv[1]) as fp:
	for line in fp:
		if "VULNERABLE" in line:
			ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', line )
			if ip:
				f_all.write(ip[0]+"','")
				#print ip[0]
				if "x86" in line:
					f_x86.write(ip[0]+"','")
				elif "x64" in line:
					f_x64.write(ip[0]+"','")
				else:
					f_unknown.write(ip[0]+"','")

f_x64.close()
f_x86.close()
f_unknown.close()



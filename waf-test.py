import sys
import requests
import time
import json

if len(sys.argv) == 1:
	print("Error:")
	print("Usage: python {} URL".format(sys.argv[0]))
	exit(1)

url = sys.argv[1] # url or path 
f = open("payload/samos_basicfuzz.txt","r") # open payload file, "r" is read only mode

request_count	= 0 # variable used to count number of requests/payloads
success_count 	= 0 # variable used to count success requests (send on uptime and)
failed_count 	= 0 # variable used to count fail requests (send on downtime or other fail)
allowed_count 	= 0 # variable used to count allowed requests
blocked_count 	= 0 # variable used to count blocked requests
error_count 	= 0 # variable used to count error requests

PASS = []

for w in f:
	request_count += 1
	print('> GET {}{}'.format(url, w.strip()))
	try:
		r = requests.get(url, params=w)
		print("< status_code = {}".format(r.status_code))
		success_count += 1
		if r.status_code == 200:
			allowed_count += 1
			PASS.append(w)
		elif r.status_code == 403:
			#print w #print payloads/requests was blocked by cloudfront
			blocked_count += 1
		else:
			print('** Failed: status_code={}, Payload: {}'.format(r.status_code, w))
	except Exception as e:
		failed_count += 1

	#time.sleep(0.1)

print("\n")
print('## WAF Testing on {} ##'.format(url))
print('  Total requests: {:>6,} requests'.format(request_count))
print('Success requests: {:>6,} requests'.format(success_count))
print(' Failed requests: {:>6,} requests'.format(failed_count))
print('Allowed requests: {:>6,} requests'.format(allowed_count))
print('Blocked requests: {:>6,} requests'.format(blocked_count))
print("\n")

f.close()

f_pass = open('pass.json', 'w')
f_pass.write(json.dumps(PASS, indent=2, ensure_ascii=False))
f_pass.close()


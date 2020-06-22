import sys
from opencage.geocoder import OpenCageGeocode, InvalidInputError, RateLimitExceededError, UnknownError
from pprint import pprint

key = 'eb30b2989ff243a8a7e3a670621c93ab'
geocoder = OpenCageGeocode(key)
#addressfile = [sys.argv[1] + ', indonesia']

def get(address):
	try:
		for line in addressfile:
			address = line.strip()
			results = geocoder.geocode(address, no_annotations='1')
			pprint(results)
			print("-"*110)
			if result and len(result):
				longitude = result[0]['geometry']['lng']
				latitude  = result[0]['geometry']['lat']
				print(u'%f;%f;%s' % (latitude, longitude, address))
				reverse_results = geocoder.reverse_geocode(latitude, longitude)
				pprint(reverse_results)
				# 40.416705;-3.703582;Madrid,Spain
				# 45.466797;9.190498;Milan,Italy
				# 52.517037;13.388860;Berlin,Germany
				return results, reverse_results
			else:
				sys.stderr.write("not found: %s\n" % address)
	except IOError:
		print('Error: File %s does not appear to exist.' % addressfile)
	except RateLimitExceededError as ex:
		print(ex)
	return False, False
	# Your rate limit has expired. It will reset to 2500 at midnight UTC timezone
	# Upgrade on https://opencagedata.com/pricing

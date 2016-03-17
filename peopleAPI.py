import requests, json, sys
import time

headers = {'User-Agent': 'Briz'}
key1 = 'ea0599c31671b3618d242e3507b01fd30bb087be'
key2 = 'fe6b1f29255d42fcefbde1fc09b7c5490c964aca'
key3 = 'a803508503db9e227b2da5ef96845e78725e6614'
key4 = '946c1b3ccc6574bf7d9ea40733b45c8b6bc2a3e7'
git@github.com:brpowell/cs373-idb.git
f = open('people.json', 'r')
d = json.load(f)
gameID = 148899
maxID = 163760
key = key1
write = True

num = 0
#154375
while gameID < maxID :
	try :
		url = 'http://www.giantbomb.com/api/person/3040-' + str(gameID) + '/?api_key=' + key + '&format=json&field_list=id,name,birth_date,country,death_date,deck,games,gender,hometown,people,first_credited_game'
		r = requests.get(url, headers=headers)

		print(gameID)

		if num == 50 :
			if key == key1 :
				key = key2
			elif key == key2 :
				key = key3
			elif key == key3 :
				key = key4
			elif key == key4 :
				key = key1
			num = 0


		if r.json()['error'] == 'Rate limit exceeded.  Slow down cowboy.' :
			if key == key1 :
				key = key2
			elif key == key2 :
				key = key3
			elif key == key3 :
				key = key4
			elif key == key4 :
				key = key1
			time.sleep(2)
			gameID -= 1	

		if r.json()['error'] != 'Object Not Found' and r.json()['error'] != 'Rate limit exceeded.  Slow down cowboy.':
			d[str(gameID)] = r.json()['results']
		
		gameID += 1
		num += 1

	except :
		f = open('people.json', 'w')
		data = json.dumps(d)
		f.write(data)
		f.close()
		write = False
		print('error with gameID: ' + str(gameID))
		break

if write :
	f = open('people.json', 'w')
	data = json.dumps(d)
	f.write(data)
	f.close()




import json
import time
from normalize import normalize_tweets
from classify import TweetClassifier
from extract import AddressExtractor
import geopy

with open('struckdc.json') as f:
    data = json.load(f)

tweets = [tweet['text'] for tweet in data]

print("Starting with " + str(len(tweets)) + " tweets")

classifier = TweetClassifier()
tweets = [x for x in tweets if classifier.classify(x)]
print("After removing tweets not starting with #ddd: " + str(len(tweets)))

tweets = normalize_tweets(tweets)

extractor = AddressExtractor()
addresses = []
for index, tweet in enumerate(tweets):
    address = extractor.extract(tweet)
    if address:
        addresses.append(address)
print("Number of addresses: " + str(len(addresses)))

geolocator = geopy.geocoders.GoogleV3()
coords = []
for x in addresses:
    time.sleep(0.3)
    try:
        address, (latitude, longitude) = geolocator.geocode(x + " Washington DC")
    except Exception as e:
        # probably a temporary wireless network fluke
        print("unknown error: going to sleep for 5 seconds")
        print(e.message)
        time.sleep(5)

    if address == 'Washington, DC, USA':
        # could not geocode the address
        continue
    coords.append((latitude, longitude))

print("Number of coordinates: " + str(len(coords)))

with open('data.json', 'w') as outfile:
    outfile.write('data = ')
    json.dump(coords, outfile)
    outfile.write(';')

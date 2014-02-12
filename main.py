import json
import time
import re
from normalize import normalize_text
from classify import TweetClassifier
from extract import AddressExtractor
import geopy

with open('tweets.json') as f:
    data = json.load(f)

tweets = [{key: tweet[key] for key in ['text', 'created_at']} for tweet in data]

print("Starting with " + str(len(tweets)) + " tweets")

classifier = TweetClassifier()
tweets = [x for x in tweets if classifier.classify(x['text'])]
print("After removing tweets not starting with #ddd: " + str(len(tweets)))

extractor = AddressExtractor()
for tweet in tweets:
    tweet['text'] = normalize_text(tweet['text'])
    # cheap classifier for pedestrian versus cyclist
    tweet['cyclist'] = bool(re.search(r'(?i)cycl', tweet['text']))
    tweet['address'] = extractor.extract(tweet['text'])

geolocator = geopy.geocoders.GoogleV3()
for tweet in tweets:
    # throttling
    time.sleep(0.3)

    if tweet['address'] is None:
        continue

    try:
        address, (latitude, longitude) = geolocator.geocode(tweet['address'] + " Washington DC")
    except Exception as e:
        # probably a temporary wireless network fluke - skipping tweet
        print("unknown error: going to sleep for 5 seconds")
        print(e.message)
        tweet['address'] = None
        time.sleep(5)
        continue

    # getting just DC back means geocoding failed
    if address != 'Washington, DC, USA':
        tweet['address'] = address
        tweet['latitude'] = latitude
        tweet['longitude'] = longitude
    else:
        print("Error: could not geocode " + tweet['address'])
        tweet['address'] = None


# remove tweets that we did not get addresses and lat/lon for
tweets = [tweet for tweet in tweets if tweet['address'] is not None]
print("Number of addresses: " + str(len(tweets)))

with open('struckdc.json', 'w') as outfile:
    json.dump(tweets, outfile)

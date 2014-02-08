import re


def normalize_tweets(tweets):
    """Clean up tweet text before running through POS tagger"""

    # remove urls
    # hack for: #313 Submission: Cyclist Struck at 403 New Jersey Ave NWhttp://wp.me/pXPcJ-3Q (6/22)
    tweets = [x.replace('http://wp.me/pXPcJ-3Q', '') for x in tweets]
    tweets = [remove_urls(x) for x in tweets]

    # remove . and , to not confuse address parsing
    tweets = [x.replace(',', ' ') for x in tweets]
    tweets = [x.replace('.', ' ') for x in tweets]
    tweets = [x.replace('  ', ' ') for x in tweets]

    tweets = normalize_abbrs(tweets)

    # fix encoding
    tweets = [x.replace('&amp;', '&') for x in tweets]

    tweets = [re.sub(r'(?i)\bped\b', 'pedestrian', x) for x in tweets]

    # put a space between streen number and blk
    blk_pat = re.compile('(?<=\d)blk')
    for index, tweet in enumerate(tweets):
        matches = blk_pat.findall(tweet)
        if matches:
            tweets[index] = tweet.replace('blk', ' blk')

    return tweets


def remove_urls(text):
    """Remove URLs from text"""

    #See: http://daringfireball.net/2010/07/improved_regex_for_matching_urls
    url_pat = re.compile(ur'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')

    matches = url_pat.findall(text)
    for x in matches:
        text = text.replace(x[0], '')

    return text


def normalize_abbrs(tweets):
    """Expand abbreviations related to locations in tweets"""

    tweets = [re.sub(r'(?i)\bave\b', 'Avenue', x) for x in tweets]
    tweets = [re.sub(r'(?i)\bav\b', 'Avenue', x) for x in tweets]
    tweets = [re.sub(r'(?i)\bst\b', 'Street', x) for x in tweets]
    tweets = [re.sub(r'(?i)\bsts\b', 'Streets', x) for x in tweets]
    tweets = [re.sub(r'(?i)\brd\b', 'Road', x) for x in tweets]
    tweets = [re.sub(r'(?i)\bdr\b', 'Drive', x) for x in tweets]
    tweets = [re.sub(r'(?i)\bpl\b', 'Place', x) for x in tweets]

    tweets = [re.sub(r'(?i)\bSe\b', 'SE', x) for x in tweets]
    tweets = [re.sub(r'(?i)\bSw\b', 'SW', x) for x in tweets]
    tweets = [re.sub(r'(?i)\bNe\b', 'NE', x) for x in tweets]
    tweets = [re.sub(r'(?i)\bNw\b', 'NW', x) for x in tweets]

    tweets = [re.sub(r'\bCap\b', 'Capitol', x) for x in tweets]
    tweets = [re.sub(r'\bSo\b', 'South', x) for x in tweets]
    tweets = [x.replace('NYAv', 'NY Avenue') for x in tweets]

    return tweets
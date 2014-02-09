# -*- coding: utf-8 -*-
import re


def normalize_tweets(tweets):
    """Clean up tweet text before running through POS tagger"""

    # fix typos
    tweets = [x.replace(u'—', ' ') for x in tweets]
    tweets = [x.replace('-', ' ') for x in tweets]
    tweets = [x.replace('  ', ' ') for x in tweets]
    tweets = [x.replace('&amp;', '&') for x in tweets]
    tweets = [x.replace('14thSt', '14th St') for x in tweets]
    tweets = [x.replace('blkTaylor', 'blk Taylor') for x in tweets]
    tweets = [x.replace('k St', 'K St') for x in tweets]
    tweets = [x.replace(' street ', ' Street ') for x in tweets]
    tweets = [x.replace('S Cap SE', 'South Capitol Street SE') for x in tweets]
    tweets = [x.replace('RESERVOIR RD', 'Reservoir Road') for x in tweets]
    tweets = [x.replace('Rhode island', 'Rhode Island') for x in tweets]
    tweets = [x.replace('3500blK', '3500 blk') for x in tweets]
    tweets = [x.replace('13TH', '13th') for x in tweets]
    tweets = [x.replace('14 &', '14th Street &') for x in tweets]
    tweets = [x.replace('15 &', '15th &') for x in tweets]
    tweets = [x.replace('15h', '15th') for x in tweets]
    tweets = [x.replace('17TH', '17th') for x in tweets]
    tweets = [x.replace('17 th', '17th') for x in tweets]
    tweets = [x.replace('17 &', '17th &') for x in tweets]
    tweets = [x.replace('17th & independence', '17th Street & Independence') for x in tweets]
    tweets = [x.replace('Nannie helen Burroughs', 'Nannie Helen Burroughs') for x in tweets]
    tweets = [x.replace('struck-33rd', 'struck - 33rd') for x in tweets]
    tweets = [x.replace('Penn v', 'Penn Avenue') for x in tweets]
    tweets = [x.replace('2600 Bowen SE', '2600 Bowen Road SE') for x in tweets]
    tweets = [x.replace('6th&MStNW', '6th & M St NW') for x in tweets]
    tweets = [x.replace('//1300', '1300') for x in tweets]
    tweets = [x.replace('b&', '&') for x in tweets]
    tweets = [x.replace('Conn Av.&', 'Conn Avenue &') for x in tweets]
    tweets = [x.replace('otis St', 'Otis Street') for x in tweets]
    tweets = [x.replace('independence', 'Independence') for x in tweets]
    tweets = [x.replace('irving', 'Irving') for x in tweets]
    tweets = [x.replace('Mt pleasant', 'Mt Pleasant') for x in tweets]
    tweets = [x.replace('ERastern', 'Eastern') for x in tweets]
    tweets = [x.replace('CONSTITUTION', 'Constitution') for x in tweets]
    tweets = [x.replace('WOODLEY', 'Woodley') for x in tweets]
    tweets = [x.replace('GALLATIN', 'Gallatin') for x in tweets]
    tweets = [x.replace('NEW HAMPSHIRE', 'New Hampshire') for x in tweets]
    tweets = [x.replace('TAYLOR', 'Taylor') for x in tweets]
    tweets = [x.replace('NW/', 'NW - ') for x in tweets]
    tweets = [x.replace('NE:', 'NE :') for x in tweets]
    tweets = [x.replace('Ne:', 'Ne :') for x in tweets]
    tweets = [x.replace('NW:', 'NW :') for x in tweets]
    tweets = [x.replace('Nw:', 'NW :') for x in tweets]
    tweets = [x.replace('Nw:', 'NW :') for x in tweets]
    tweets = [x.replace('SE:', 'SE :') for x in tweets]
    tweets = [x.replace('SW:', 'SW :') for x in tweets]
    tweets = [x.replace('SW/', 'SW - ') for x in tweets]
    tweets = [x.replace('b/o', 'block of') for x in tweets]
    tweets = [x.replace('NWhttp://wp.me/pXPcJ-3Q', 'NW http://wp.me/pXPcJ-3Q') for x in tweets]
    tweets = [re.sub(r' @ ', ' & ', x) for x in tweets]
    tweets = [re.sub(r'(?<=\d{2})TH', 'th', x) for x in tweets]
    tweets = [x.replace('unit block', '100 block') for x in tweets]
    tweets = [x.replace('unit blk', '100 block') for x in tweets]
    tweets = [re.sub(r'(?<!:)//', ' ', x) for x in tweets]

    # remove urls
    tweets = [remove_urls(x) for x in tweets]

    # put a space between street number and blk
    blk_pat = re.compile('(?<=\d)blk')
    for index, tweet in enumerate(tweets):
        matches = blk_pat.findall(tweet)
        if matches:
            tweets[index] = tweet.replace('blk', ' blk')

    # remove . and , to not confuse address parsing
    tweets = [x.replace(',', '') for x in tweets]
    tweets = [x.replace('.', '') for x in tweets]

    tweets = normalize_abbrs(tweets)

    # normalize case for pedestrian, cyclist, struck, bicyclist
    tweets = [re.sub(r'(?i)\bped\b', 'pedestrian', x) for x in tweets]
    tweets = [x.replace('Pedestrian', 'pedestrian') for x in tweets]
    tweets = [x.replace('Cyclist', 'cyclist') for x in tweets]
    tweets = [x.replace('Bicyclist', 'cyclist') for x in tweets]
    tweets = [x.replace('Struck', 'struck') for x in tweets]
    tweets = [x.replace('Block', 'block') for x in tweets]

    # standardize block of vs block (choosing to drop of for easier token processing)
    tweets = [x.replace('block of', 'block') for x in tweets]

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
    tweets = [re.sub(r'(?i)\bpkwy\b', 'Parkway', x) for x in tweets]
    tweets = [re.sub(r'(?i)\bblvd\b', 'Boulevard', x) for x in tweets]
    tweets = [re.sub(r'(?i)\bbl\b', 'Boulevard', x) for x in tweets]
    tweets = [re.sub(r'(?i)\bblk\b', 'block', x) for x in tweets]

    tweets = [re.sub(r'(?i)\bSe\b', 'SE', x) for x in tweets]
    tweets = [re.sub(r'(?i)\bSw\b', 'SW', x) for x in tweets]
    tweets = [re.sub(r'(?i)\bNe\b', 'NE', x) for x in tweets]
    tweets = [re.sub(r'(?i)\bNw\b', 'NW', x) for x in tweets]

    tweets = [re.sub(r'\bCap\b', 'Capitol', x) for x in tweets]
    tweets = [re.sub(r'\bSo\b', 'South', x) for x in tweets]
    tweets = [x.replace('NYAv', 'NY Avenue') for x in tweets]

    return tweets
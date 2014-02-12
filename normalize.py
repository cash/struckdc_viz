# -*- coding: utf-8 -*-
import re


def normalize_text(text):
    """Clean up tweet text to simplify parsing"""

    text = fix_typos(text)
    text = remove_urls(text)

    # remove . and , to not confuse address parsing
    text = text.replace(',', '')
    text = text.replace('.', '')

    # put a space between street number and blk
    blk_pat = re.compile('(?<=\d)blk')
    matches = blk_pat.findall(text)
    if matches:
        text = text.replace('blk', ' blk')

    text = normalize_abbrs(text)

    # normalize case for pedestrian, cyclist, struck, bicyclist
    text = re.sub(r'(?i)\bped\b', 'pedestrian', text)
    text = text.replace('Pedestrian', 'pedestrian')
    text = text.replace('Cyclist', 'cyclist')
    text = text.replace('Bicyclist', 'cyclist')
    text = text.replace('Bicycle', 'bicycle')
    text = text.replace('Struck', 'struck')
    text = text.replace('Block', 'block')

    # standardize 'block of' vs 'block' (choosing to drop 'of' for easier token processing)
    text = text.replace('block of', 'block')

    return text


def remove_urls(text):
    """Remove URLs from text"""

    #See: http://daringfireball.net/2010/07/improved_regex_for_matching_urls
    url_pat = re.compile(ur'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')

    matches = url_pat.findall(text)
    for x in matches:
        text = text.replace(x[0], '')

    return text


def normalize_abbrs(text):
    """Expand abbreviations related to locations in tweet text"""

    text = re.sub(r'(?i)\bave\b', 'Avenue', text)
    text = re.sub(r'(?i)\bav\b', 'Avenue', text)
    text = re.sub(r'(?i)\bst\b', 'Street', text)
    text = re.sub(r'(?i)\bsts\b', 'Streets', text)
    text = re.sub(r'(?i)\brd\b', 'Road', text)
    text = re.sub(r'(?i)\bdr\b', 'Drive', text)
    text = re.sub(r'(?i)\bpl\b', 'Place', text)
    text = re.sub(r'(?i)\bcir\b', 'Circle', text)
    text = re.sub(r'(?i)\bpkwy\b', 'Parkway', text)
    text = re.sub(r'(?i)\bblvd\b', 'Boulevard', text)
    text = re.sub(r'(?i)\bbl\b', 'Boulevard', text)
    text = re.sub(r'(?i)\bblk\b', 'block', text)

    text = re.sub(r'(?i)\bSe\b', 'SE', text)
    text = re.sub(r'(?i)\bSw\b', 'SW', text)
    text = re.sub(r'(?i)\bNe\b', 'NE', text)
    text = re.sub(r'(?i)\bNw\b', 'NW', text)

    text = re.sub(r'\bCap\b', 'Capitol', text)
    text = re.sub(r'\bSo\b', 'South', text)
    text = text.replace('NYAv', 'NY Avenue')
    text = re.sub(r'\bMass\b', 'Massachusetts', text)
    text = re.sub(r'\bNY\b', 'New York', text)
    text = re.sub(r'\bNJ\b', 'New Jersey', text)
    text = re.sub(r'\bPA\b', 'Pennsylvania', text)
    text = re.sub(r'(?i)\bGA\b', 'Georgia', text)
    text = re.sub(r'(?i)\bRI\b', 'Rhode Island', text)
    text = re.sub(r'\bInd\b', 'Indiana', text)
    text = re.sub(r'\bFla\b', 'Florida', text)
    text = re.sub(r'\bConn\b', 'Connecticut', text)
    text = re.sub(r'\bNeb\b', 'Nebraska', text)
    text = re.sub(r'\bMinn\b', 'Minnesota', text)

    return text

def fix_typos(text):
    """hacky quick typo fixes"""

    text = text.replace(u'—', ' ')
    text = text.replace('-', ' ')
    text = text.replace('  ', ' ')
    text = text.replace('&amp;', '&')
    text = text.replace('14thSt', '14th St')
    text = text.replace('blkTaylor', 'blk Taylor')
    text = text.replace('k St', 'K St')
    text = text.replace(' street ', ' Street ')
    text = text.replace('S Cap SE', 'South Capitol Street SE')
    text = text.replace('RESERVOIR RD', 'Reservoir Road')
    text = text.replace('Rhode island', 'Rhode Island')
    text = text.replace('3500blK', '3500 blk')
    text = text.replace('13TH', '13th')
    text = text.replace('14 &', '14th Street &')
    text = text.replace('15 &', '15th &')
    text = text.replace('15h', '15th')
    text = text.replace('17TH', '17th')
    text = text.replace('17 th', '17th')
    text = text.replace('17 &', '17th &')
    text = text.replace('17th & independence', '17th Street & Independence')
    text = text.replace('Nannie helen Burroughs', 'Nannie Helen Burroughs')
    text = text.replace('struck-33rd', 'struck - 33rd')
    text = text.replace('Penn v', 'Penn Avenue')
    text = text.replace('2600 Bowen SE', '2600 Bowen Road SE')
    text = text.replace('6th&MStNW', '6th & M St NW')
    text = text.replace('//1300', '1300')
    text = text.replace('b&', '&')
    text = text.replace('Conn Av.&', 'Conn Avenue &')
    text = text.replace('otis St', 'Otis Street')
    text = text.replace('independence', 'Independence')
    text = text.replace('irving', 'Irving')
    text = text.replace('Mt pleasant', 'Mt Pleasant')
    text = text.replace('ERastern', 'Eastern')
    text = text.replace('CONSTITUTION', 'Constitution')
    text = text.replace('WOODLEY', 'Woodley')
    text = text.replace('GALLATIN', 'Gallatin')
    text = text.replace('NEW HAMPSHIRE', 'New Hampshire')
    text = text.replace('TAYLOR', 'Taylor')
    text = text.replace('Joeclyn', 'Jocelyn')
    text = text.replace('NW/', 'NW - ')
    text = text.replace('NE:', 'NE :')
    text = text.replace('Ne:', 'Ne :')
    text = text.replace('NW:', 'NW :')
    text = text.replace('Nw:', 'NW :')
    text = text.replace('Nw:', 'NW :')
    text = text.replace('SE:', 'SE :')
    text = text.replace('SW:', 'SW :')
    text = text.replace('SW/', 'SW - ')
    text = text.replace('b/o', 'block of')
    text = text.replace('NWhttp://wp.me/pXPcJ-3Q', 'NW http://wp.me/pXPcJ-3Q')
    text = text.replace('unit block', '100 block')
    text = text.replace('unit blk', '100 block')
    text = re.sub(r' @ ', ' & ', text)
    text = re.sub(r'\bAt\b', 'at', text)
    text = re.sub(r'(?<=\d{2})TH', 'th', text)
    text = re.sub(r'(?<!:)//', ' ', text)

    return text
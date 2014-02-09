import re


class Tokens(object):
    NUMBER = 1
    NAME = 2
    AND = 3
    STREET_TYPE = 4
    QUAD = 5
    BLOCK = 6
    OTHER = 7


class AddressExtractor(object):
    """Extract addresses from tweets

       This supports two different types of address (block address and intersections).
       It tokenizes the tweet and then implements hard coded FSMs for the two address
       types. Another option would be to convert the list of tokens to a string and
       performed regex matching on the strings.
    """

    def extract(self, tweet):
        """Extract an address from a tweet"""

        # we support two formats:
        #  1. block format: 1200 block NY Ave NW
        #  2. intersection format: 10th & U NW
        address = None
        if re.search(r' \d{3,4} ', tweet):
            address = self.extractBlock(tweet)

        if not address:
            address = self.extractIntersection(tweet)

        return address

    def extractBlock(self, tweet):
        strings = tweet.split(' ')

        # pattern to match: NUMBER BLOCK? NAME+ STREET QUAD?

        try:
            string, token = self.popToken(strings)
            while True:
                address_strings = []

                # get number token
                while token != Tokens.NUMBER:
                    string, token = self.popToken(strings)
                address_strings.append(string)

                # get street name
                string, token = self.popToken(strings)
                if token == Tokens.BLOCK:
                    # skip block token
                    string, token = self.popToken(strings)
                if token != Tokens.NAME:
                    # reset to looking for number
                    continue
                while token == Tokens.NAME:
                    address_strings.append(string)
                    string, token = self.popToken(strings)

                # street type next
                if token != Tokens.STREET_TYPE:
                    continue
                address_strings.append(string)

                # quadrant
                if len(strings):
                    string, token = self.popToken(strings)
                    if token == Tokens.QUAD:
                        address_strings.append(string)
                break

        except IndexError:
            # no strings left
            return None

        return ' '.join(address_strings)

    def extractIntersection(self, tweet):
        strings = tweet.split(' ')

        # pattern to match: NAME+ STREET? QUAD? AND NAME+ STREET? QUAD?

        tokens = [self.map(string) for string in strings]
        indexes = self.findIndex(tokens, Tokens.AND)

        while indexes:
            and_index = indexes.pop(0)
            address_strings = ['and']

            # check backward first
            index = and_index
            index -= 1

            # optional quad
            if tokens[index] == Tokens.QUAD:
                address_strings.insert(0, strings[index])
                index -= 1

            # optional street type
            if tokens[index] == Tokens.STREET_TYPE:
                address_strings.insert(0, strings[index])
                index -= 1

            # required name
            if tokens[index] != Tokens.NAME:
                continue
            while tokens[index] == Tokens.NAME:
                address_strings.insert(0, strings[index])
                index -= 1

            # forward check
            index = and_index + 1

            # required name
            if tokens[index] != Tokens.NAME:
                continue
            while index < len(tokens) and tokens[index] == Tokens.NAME:
                address_strings.append(strings[index])
                index += 1

            # optional street type
            if index < len(tokens) and tokens[index] == Tokens.STREET_TYPE:
                address_strings.append(strings[index])
                index += 1

            # optional quad
            if index < len(tokens) and tokens[index] == Tokens.QUAD:
                address_strings.append(strings[index])
            return ' '.join(address_strings)

        return None

    def map(self, string):
        """Map a string to a token"""

        if re.match(r'\d{3,4}', string):
            return Tokens.NUMBER
        elif string == '&' or string.lower() == 'and':
            return Tokens.AND
        # catch the retweet
        elif string == 'MT':
            return Tokens.OTHER
        elif string.lower() == 'block':
            return Tokens.BLOCK
        elif string in ['NE', 'NW', 'SE', 'SW']:
            return Tokens.QUAD
        elif string in ['Street', 'Avenue', 'Road', 'Circle', 'Drive',
                        'Way', 'Parkway', 'Place', 'Terrace', 'Boulevard']:
            return Tokens.STREET_TYPE
        # 1st, 2nd, etc
        elif re.match(r'\d{1,2}(st|nd|rd|th)', string):
            return Tokens.NAME
        # Street names
        elif re.match(r'[A-Z][a-z]+', string):
            return Tokens.NAME
        # single letter streets and state abbr
        elif re.match(r'[A-Z]{1,2}$', string):
            return Tokens.NAME
        elif string == 'MLK':
            return Tokens.NAME
        else:
            return Tokens.OTHER

    def popToken(self, strings):
        """Pop a string from the list and return the string and its token"""
        string = strings.pop(0)
        return string, self.map(string)

    def findIndex(self, data, item):
        """Return a list of indexes for the value in the list"""
        indexes = []

        for index, value in enumerate(data):
            if value == item:
                indexes.append(index)

        return indexes
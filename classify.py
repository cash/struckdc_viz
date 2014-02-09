import re


class TweetClassifier(object):
    """Classify whether tweet contains an address

       Stand in algorithm is to test if the tweet starts with # followed by a number
    """

    def __init__(self):
        self._count_matcher = re.compile(r'#\d{1,3}')

    def classify(self, tweet):
        return bool(self._count_matcher.match(tweet))

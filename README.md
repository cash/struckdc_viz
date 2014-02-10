Visualization of the @struckDC Twitter feed
===========================================
[@struckDC](https://twitter.com/struckDC) is a Twitter feed that records the location of accidents in DC that involve pedestrians and cyclists. A heatmap overlayed on a map of DC is viewable at http://cash.github.io/struckdc_viz/.

The tweets were pulled down using [tweetvac](https://github.com/cash/tweetvac). The addresses were geocoded to latitude and longitude using [geopy](https://github.com/geopy/geopy). The heatmap was created using the Google Maps Visualization API. The code for normalizing the text and extracting the addresses from the tweet text is in this repository.

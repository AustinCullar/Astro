# Astro
Automated data collection from YouTube.

# Background
YouTube has been a primary source of information and entertainment in my house
for years now. Recently when looking at the comments of various videos, I've
noticed what I feel is strange behavior. However, I am not someone who regularly
engages with social media in that way, so this project is my attempt to
investigate and understand the behavior I see online.

The name 'Astro' was chosen as a short form of 'Astroturf', a term used to
describe artificial social movements, since I was initially working toward
identifying bot campaigns. I've since decided to restrict the scope of the
project (at least for now), since that goal will require much more research.

# Prerequisites
These packages are required in order to run this tool.

- YouTube Data API
Used for accessing YouTube data. Install with:
`pip install google-api-python-client`

- dotenv
Used for loading environment variables from a local .env file. Install with:
`pip insatll python-dotenv`

- pandas
Used for capturing YouTube data in dataframes (for now). Install with:
`pip install pandas`

- Natural Language Toolkit
Used for sentiment analysis of comments. Install with:
`pip insatll nltk`

# Overview
This project is focused on collecting data from YouTube via the Data API.

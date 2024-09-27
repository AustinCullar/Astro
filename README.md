# Astro
Automated data collection from YouTube.

## Overview
This project is focused on collecting data from YouTube via the Data API.
Currently, this tool will collect comment info from the provided video ID
string, storing the data into an sqlite database file.

The comment data collected includes:
- author
- text
- timestamp

Sentiment analysis is performed on the comment text using the 'nltk' (Natural
Language Toolkit) python library. This data is added to the database entries of
each comment.

## Setup Instructions
1. Install `python3`
2. Create your python virtual environment with `python3 -m venv <env name>`
3. Install the packages in the `src/requirements.txt` file to your virtual
   environment with `pip install -r requirements.txt`.
4. Create a file in the `/src` directory called `.env`. This file should contain
   The following values:
   ```
    API_KEY=<key> # your YouTube Data API key
    DB_FILE=<filename> # the database file to which collected data will be written
    LOG_LEVEL=[debug|info|warn|error]
    ```
    For information about how to create an API key, see [here](https://blog.hubspot.com/website/how-to-get-youtube-api-key).
5. Run the tool with `python astro.py <YouTube video URL>` to start collecting
   data. You can see output from an example run in the next section.

## Example
This output below was generated by providing the video ID string of a relatively
small YouTube channel.
```
(astro) $ python astro.py 'https://www.youtube.com/watch?v=HthY7qxV8q0' -l debug
INFO:__init__.py:autodetect: file_cache is only supported with oauth2client<4.0.0
DEBUG:discovery.py:method: URL being requested: GET https://youtube.googleapis.com/youtube/v3/commentThreads?part=snippet%2Creplies&videoId=HthY7qxV8q0&textFormat=plainText&key=<...>&alt=json
DEBUG:astro.py:main: Collected data preview:
                                             comment                user                  date PSentiment NSentiment
0  Giant keys dorp twice as often in the wilderne...      @selkokieli843  2024-09-23T19:06:29Z        0.0       0.25
1  wilderness is the way to go here. cannon isnt ...          @breaddboy  2024-09-23T18:46:20Z        0.0      0.125
2  The description is about mossy keys and Bryoph...            @MrRXY11  2024-09-23T16:49:55Z        0.0        0.0
3  no it's not you're crazy. gaslighting isn't re...           @Spookdog  2024-09-23T19:18:19Z        0.0      0.625
4  Easier way imo is in the giants den with a zar...  @jakeparkinson9639  2024-09-23T16:32:56Z        0.0        0.0
5                                              First         @HeyItsVarn  2024-09-23T16:05:07Z        0.0        0.0
```

## Background
YouTube has been a primary source of information and entertainment in my house
for years. I've found that when reading comments on YouTube videos, I'm often 
perplexed by the content there. Wanting to understand this behavior, whether it
was the product of real users or bots, I started researching social media usage.
This project is my attempt to gather data from YouTube videos and their comments
in order to analyze trends in the data, if any, in an effort to better
understand YouTube commenting behavior and its impact on video performance.

The name 'Astro' was chosen as a short form of 'Astroturf', a term used to
describe artificial social movements, since I was initially working toward
identifying bot campaigns. I've since decided to restrict the scope of the
project (at least for now), since that goal will require much more research.

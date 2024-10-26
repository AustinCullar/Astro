![CI build](https://github.com/AustinCullar/Astro/actions/workflows/astro-testing.yml/badge.svg) ![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

# Astro
Automated data collection from YouTube.

## Overview
This project is focused on collecting data from YouTube via the Data API.
Currently, this tool will collect comment info from the provided YouTube video
URL and store the data into an sqlite database file.

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
3. Install the packages in the `requirements.txt` file to your virtual
   environment with `pip install -r requirements.txt`.
4. Run `pip install -e .` to install the project packages. For developers, run
   `pip install -e pip install -e '.[dev]'` to install all test dependencies as
   well.
5. Create a file in the `/src` directory called `.env`. This file should contain
   The following values:
    ```
    API_KEY=<key> # your YouTube Data API key
    DB_FILE=<filename> # the database file to which collected data will be written
    LOG_LEVEL=[debug|info|warn|error]
    ```
    For information about how to create an API key, see [here](https://blog.hubspot.com/website/how-to-get-youtube-api-key).

    Alternatively, these values can be passed to Astro on the command line. See
    the help menu below for more information.
    ```
    (astro) $ python astro.py --help
    Usage: astro.py [-h] [-l {debug,info,warn,error}] [--api-key API_KEY] [--db-file DB_FILE] [--log-file LOG_FILE]
                    [-j | --log-json | --no-log-json]
                    youtube_url

    A tool for YouTube data collection.

    Positional Arguments:
      youtube_url           youtube video URL

    Options:
      -h, --help            show this help message and exit
      -l, --log {debug,info,warn,error}
                            Set the logging level (default: info)
      --api-key API_KEY     YouTube Data API key (default: None)
      --db-file DB_FILE     database filename (default: astro.db)
      --log-file LOG_FILE   log output to specified file (default: astro_log.txt)
      -j, --log-json, --no-log-json
                            log json API responses (default: False)
    ```
6. Run the tool with `python astro.py <YouTube video URL>` to start collecting
   data. You can see output from an example run in the next section.

## Example
This output below was generated using a YouTube video URL from user 'hbomberguy'.
```
(astro) $ python astro.py 'https://www.youtube.com/watch?v=0twDETh6QaI'
[10/26/24 11:56:52] INFO                 video_id: 0twDETh6QaI                                                       log.py:119
                    INFO              video_title: ROBLOX_OOF.mp3                                                    log.py:119
                    INFO               channel_id: UClt01z1wHHT7c5lKcU8pxRQ                                          log.py:119
                    INFO            channel_title: hbomberguy                                                        log.py:119
                    INFO               view_count: 13852769                                                          log.py:119
                    INFO               like_count: 398474                                                            log.py:119
                    INFO            comment_count: 46258                                                             log.py:119
                    INFO        comments_disabled: False                                                             log.py:119
Downloading comments 100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 46258/46258 • 0:03:02 • 0:00:00
Calculating comment sentiment 100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 39643/39643 • 0:00:53 • 0:00:00
[10/26/24 12:00:48] INFO     Video has filtered 14.30% of comments                                                  astro.py:91
                                                     Comment data preview
                                                            ...
```

By default, Astro will log output to a file named `./astro_log.txt` unless
otherwise specified by the `--log-file` option or the `LOG_FILE` environment
variable.

## Background
YouTube has been a primary source of information and entertainment in my house
for years. I've found that when reading comments on YouTube videos, I'm often
confused by the content there. Wanting to understand this behavior, whether it
was the product of real users or bots, I started researching social media usage.
This project is my attempt to gather data from YouTube videos and their comments
in order to analyze trends in the data, if any, in an effort to better
understand YouTube commenting behavior and its impact on video performance.

The name 'Astro' was chosen as a short form of 'Astroturf', a term used to
describe artificial social movements, since I was initially working toward
identifying bot campaigns. I've since decided to restrict the scope of the
project (at least for now), since that goal will require much more research.

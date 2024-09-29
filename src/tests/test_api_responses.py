"""
This file contains example YouTube Data API responses for use
in testing.
"""


test_comment_api_response = """
{
    "kind": "youtube#commentThreadListResponse",
    "etag": "Leymzj7IilCkKdGveEdfycOes08",
    "pageInfo": {
        "totalResults": 5,
        "resultsPerPage": 20
    },
    "items": [
        {
            "kind": "youtube#commentThread",
            "etag": "x6PsyLYZI_5JIZ2iZcqnArGXYSs",
            "id": "UgxXfLfuryhN5JBV4Zl4AaABAg",
            "snippet": {
                "channelId": "UC8-VPb0BrTumJCcAk5kKD8w",
                "videoId": "HthY7qxV8q0",
                "topLevelComment": {
                    "kind": "youtube#comment",
                    "etag": "rOelwfDwMkMGoSFRL1gwMUYONWE",
                    "id": "UgxXfLfuryhN5JBV4Zl4AaABAg",
                    "snippet": {
                        "channelId": "UC8-VPb0BrTumJCcAk5kKD8w",
                        "videoId": "HthY7qxV8q0",
                        "textDisplay": "test comment",
                        "textOriginal": "test comment",
                        "authorDisplayName": "@test_user",
                        "authorProfileImageUrl": "https://yt3.ggpht.com/ytc/AIdro_kAzIIBv7Rh-9lcOg8Q2E6YYFE2O0ajm4eVWfxcqUE=s48-c-k-c0x00ffffff-no-rj",
                        "authorChannelUrl": "http://www.youtube.com/@selkokieli843",
                        "authorChannelId": {
                            "value": "UCINOM9YliYsdtygvrjeT_Pg"
                        },
                        "canRate": true,
                        "viewerRating": "none",
                        "likeCount": 0,
                        "publishedAt": "2024-09-23T19:06:29Z",
                        "updatedAt": "2024-09-23T19:06:29Z"
                    }
                },
                "canReply": true,
                "totalReplyCount": 1,
                "isPublic": true
            },
            "replies": {
                "comments": [
                    {
                        "kind": "youtube#comment",
                        "etag": "7a1LTkhCA-krrQFfk61CH12dB_k",
                        "id": "UgxXfLfuryhN5JBV4Zl4AaABAg.A8jq-geGgIoA8k_tlJmJ7O",
                        "snippet": {
                            "channelId": "UC8-VPb0BrTumJCcAk5kKD8w",
                            "videoId": "HthY7qxV8q0",
                            "textDisplay": "test reply",
                            "textOriginal": "test_reply",
                            "parentId": "UgxXfLfuryhN5JBV4Zl4AaABAg",
                            "authorDisplayName": "@testreplier",
                            "authorProfileImageUrl": "https://yt3.ggpht.com/ytc/AIdro_m7vzwjC2MSutVaniIzcgzQ59RfBF-ul3eWm8IQTks=s48-c-k-c0x00ffffff-no-rj",
                            "authorChannelUrl": "http://www.youtube.com/@testreplier",
                            "authorChannelId": {
                                "value": "UCKwXRwa85ANLLkKTWVypkAQ"
                            },
                            "canRate": true,
                            "viewerRating": "none",
                            "likeCount": 0,
                            "publishedAt": "2024-09-24T02:04:58Z",
                            "updatedAt": "2024-09-24T02:04:58Z"
                        }
                    }
                ]
            }
        }
    ]
}
"""

test_video_api_response = r"""
{
    "kind": "youtube#videoListResponse",
    "etag": "b1LCdoi5tZoD2QVWGfEwrBMl6kM",
    "items": [
        {
            "kind": "youtube#video",
            "etag": "Jq8OGlP38GvGOsSFFAm-KdrOKGc",
            "id": "HthY7qxV8q0",
            "snippet": {
                "publishedAt": "2024-09-23T16:00:14Z",
                "channelId": "UC8-VPb0BrTumJCcAk5kKD8w",
                "title": "Ironman Obor guide | Hill giants 400 KC/HR guide (no cannon)",
                "description": "This guide/loot video is for the ironmen and UIMs out there who can't use a cannon and want to go for the hill giant club! In this video I show how much hill giant KC you can get in an hour and how many giant keys that will get you, and calculated how many hours it would take to reach the drop rate.\n\nTwitter: https://twitter.com/spookpuppy\nTwitch: https://www.twitch.tv/spookdog\nIRL: https://youtube.com/@karaintheclouds\n\nSong used: Expanse https://youtu.be/0gt-mK_ZV0o?si=pB2NjMdN7bm2-R_b\n\nIf you want to join a chill osrs kinda discord server with friends who have a weird sense of humor and competitions/events like the monthly fashionscape competition, I made a server! Don't be shy about joining if you're looking to make friends, we don't bite! The only requirements to join are to be a good boi, and be over 18.\nWe're very LGBTQ+ friendly and a safe space for anyone who isn't a meanie. \u2764\nClick here to join: https://discord.com/invite/spookdog\n\nI\u2019m in the cc \"Mudkip\" and don\u2019t want to leave, but you can join my friends chat. Feel free to say hi to me c: IGN: Spookdog\n\nIf you want to support the channel, you can join to get some special perks! Don't feel obligated to, but it helps \u2665\nhttps://www.youtube.com/channel/UC8-VPb0BrTumJCcAk5kKD8w/join\n\nI\u2019ve also started a Ko-fi if you want to donate a bit, not as a monthly thing. Also not necessary but helps :) https://ko-fi.com/spookdog",
                "thumbnails": {
                    "default": {
                        "url": "https://i.ytimg.com/vi/HthY7qxV8q0/default.jpg",
                        "width": 120,
                        "height": 90
                    },
                    "medium": {
                        "url": "https://i.ytimg.com/vi/HthY7qxV8q0/mqdefault.jpg",
                        "width": 320,
                        "height": 180
                    },
                    "high": {
                        "url": "https://i.ytimg.com/vi/HthY7qxV8q0/hqdefault.jpg",
                        "width": 480,
                        "height": 360
                    },
                    "standard": {
                        "url": "https://i.ytimg.com/vi/HthY7qxV8q0/sddefault.jpg",
                        "width": 640,
                        "height": 480
                    },
                    "maxres": {
                        "url": "https://i.ytimg.com/vi/HthY7qxV8q0/maxresdefault.jpg",
                        "width": 1280,
                        "height": 720
                    }
                },
                "channelTitle": "Spookdog",
                "tags": [
                    "osrs",
                    "rs",
                    "oldschool runescape",
                    "old school runescape",
                    "obor",
                    "hill giant",
                    "giant key",
                    "giant keys",
                    "hill giant club",
                    "hill giants",
                    "f2p",
                    "money making",
                    "no cannon"
                ],
                "categoryId": "20",
                "liveBroadcastContent": "none",
                "localized": {
                    "title": "Ironman Obor guide | Hill giants 400 KC/HR guide (no cannon)",
                    "description": "This guide/loot video is for the ironmen and UIMs out there who can't use a cannon and want to go for the hill giant club! In this video I show how much hill giant KC you can get in an hour and how many giant keys that will get you, and calculated how many hours it would take to reach the drop rate.\n\nTwitter: https://twitter.com/spookpuppy\nTwitch: https://www.twitch.tv/spookdog\nIRL: https://youtube.com/@karaintheclouds\n\nSong used: Expanse https://youtu.be/0gt-mK_ZV0o?si=pB2NjMdN7bm2-R_b\n\nIf you want to join a chill osrs kinda discord server with friends who have a weird sense of humor and competitions/events like the monthly fashionscape competition, I made a server! Don't be shy about joining if you're looking to make friends, we don't bite! The only requirements to join are to be a good boi, and be over 18.\nWe're very LGBTQ+ friendly and a safe space for anyone who isn't a meanie. \u2764\nClick here to join: https://discord.com/invite/spookdog\n\nI\u2019m in the cc \"Mudkip\" and don\u2019t want to leave, but you can join my friends chat. Feel free to say hi to me c: IGN: Spookdog\n\nIf you want to support the channel, you can join to get some special perks! Don't feel obligated to, but it helps \u2665\nhttps://www.youtube.com/channel/UC8-VPb0BrTumJCcAk5kKD8w/join\n\nI\u2019ve also started a Ko-fi if you want to donate a bit, not as a monthly thing. Also not necessary but helps :) https://ko-fi.com/spookdog"
                },
                "defaultAudioLanguage": "en-US"
            },
            "contentDetails": {
                "duration": "PT3M53S",
                "dimension": "2d",
                "definition": "hd",
                "caption": "false",
                "licensedContent": true,
                "contentRating": {},
                "projection": "rectangular"
            },
            "statistics": {
                "viewCount": "983",
                "likeCount": "63",
                "favoriteCount": "0",
                "commentCount": "8"
            }
        }
    ],
    "pageInfo": {
        "totalResults": 1,
        "resultsPerPage": 1
    }
}
"""

test_empty_api_response = "{}"

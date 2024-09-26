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

test_empty_api_response = "{}"

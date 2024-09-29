"""
Classes/structures used in data collection.
"""


class VideoData:
    video_id: str
    channel_id: str
    channel_title: str
    view_count: int
    like_count: int
    comment_count: int

    def __init__(
            self,
            video_id='',
            channel_id='',
            channel_title='',
            view_count=0,
            like_count=0,
            comment_count=0):

        self.video_id = video_id
        self.channel_id = channel_id
        self.channel_title = channel_title
        self.view_count = 0
        self.like_count = 0
        self.comment_count = 0

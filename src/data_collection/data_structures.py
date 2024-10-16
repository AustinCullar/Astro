"""
Classes/structures used in data collection.
"""


class VideoData:
    video_id: str
    video_title: str
    channel_id: str
    channel_title: str
    view_count: int
    like_count: int
    comment_count: int
    comments_disabled: bool
    filtered_comment_count: int

    def __init__(
            self,
            video_id='',
            video_title='',
            channel_id='',
            channel_title='',
            view_count=0,
            like_count=0,
            comment_count=0,
            comments_disabled=False,
            filtered_comment_count=0):

        self.video_id = video_id
        self.video_title = video_title
        self.channel_id = channel_id
        self.channel_title = channel_title
        self.view_count = view_count
        self.like_count = like_count
        self.comment_count = comment_count
        self.comments_disabled = comments_disabled
        self.filtered_comment_count = filtered_comment_count

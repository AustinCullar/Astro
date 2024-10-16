from src.data_collection.data_structures import VideoData

test_video_data = [VideoData(video_id='e-qUSPnOlbb',
                             channel_id='itXtJBHdZchKKjlnVrjXeCln',
                             channel_title='YouTube_User1',
                             view_count=0,
                             like_count=0,
                             comment_count=0),
                   VideoData(video_id='whautOBEjLTM',
                             channel_id='FvlvKP-khoFMOeyBzmXuaazd',
                             channel_title='TestUser',
                             view_count=775,
                             like_count=212,
                             comment_count=0),
                   VideoData(video_id='Sc_GwhJVdhRY',
                             channel_id='LTO_OySEsmnRtoK-bkAeWXjW',
                             channel_title='User_YT99',
                             view_count=12345,
                             like_count=66423,
                             comment_count=76123),
                   # case where an invalid video_id string is provided
                   VideoData(video_id='bad data',
                             channel_id='bad data',
                             channel_title='bad data'),
                   # empty data set case
                   VideoData(video_id='',
                             channel_id='',
                             channel_title=''),
                   None]

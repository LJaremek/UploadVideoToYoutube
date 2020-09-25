# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 2020

@author: Lukasz
"""

import datetime

from Google import Create_Service
from googleapiclient.http import MediaFileUpload

def get_categories_ID(api_key: str) -> dict:
    from apiclient.discovery import build
    youtube_object = build("youtube", "v3", developerKey = api_key)
    video_id_dict = {}
    info_dict = youtube_object.videoCategories().list(part = "snippet", regionCode = "PL").execute()
    info_list = info_dict.get("items", [])
    for part_info in info_list:
        key = part_info["id"]
        value = part_info["snippet"]["title"]
        video_id_dict[key] = value
    return video_id_dict

class upload:
    def __init__(self, CLIENT_SECRET_FILE):
        self.CLIENT_SECRET_FILE = CLIENT_SECRET_FILE
        self.API_NAME = "youtube"
        self.API_VERSION = "v3"
        self.SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
        
        self.service = Create_Service(self.CLIENT_SECRET_FILE, 
                                      self.API_NAME, 
                                      self.API_VERSION, 
                                      self.SCOPES)
        
        self.upload_time = datetime.datetime(2020, 1, 1, 12, 30, 0).isoformat() + ".000Z"
        
    def __config_snippet(self,
                       title: str,
                       description: str,
                       tags: list,
                       categoryID: int):
        
        self.snippet = {"title" : title,
                        "description" : description,
                        "tags" : tags,
                        "categoryID" : categoryID}
        
    def __config_status(self,
                      privacyStatus: str):

        self.status = {"privacyStatus" : privacyStatus,
                       "publishAt" : self.upload_time,
                       "selfDeclaredMadeForKids" : False}
        
    def __config_request_body(self):
        self.request_body = {"snippet" : self.snippet,
                             "status" : self.status,
                             "notifySubscribers" : False}
        
    def upload(self,
               title: str = "title",
               description: str = "description",
               tags: list = [],
               categoryID: int = 1,
               privacyStatus: str = "private",
               video_file_name: str = "*.mp4",
               media_body_file_name: str = "*.png"):
    
        self.__config_snippet(title, description, tags, categoryID)
        self.__config_status(privacyStatus)
        self.__config_request_body()
    
    
        self.video_file_name = video_file_name
        
        self.media_file = MediaFileUpload(self.video_file_name)
        
        self.response_upload = self.service.videos().insert(
            part = "snippet,status",
            body = self.request_body,
            media_body = self.media_file).execute()
        
        
        self.service.thumbnails().set(
            videoId = self.response_upload.get("id"),
            media_body = MediaFileUpload(media_body_file_name)).execute()

# CLIENT_SECRET_FILE = "client_secret_number.json"

# video_upload = upload(CLIENT_SECRET_FILE)
# video_upload.upload("tytul filmu",
#                     "opis filmu",
#                     ["tag 1", "tag 2"],
#                     1,
#                     "public",
#                     "film.mp4",
#                     "miniaturka.png")

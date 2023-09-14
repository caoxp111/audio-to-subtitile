from enum import Enum

FILE_PATH_SEPARATOR = '/'
SRT_EXTENSION = '.srt'
MP3_EXTENSION = '.mp3'
MP4_EXTENSION = '.mp4'
PDF_EXTENSION = '.pdf'


class FileCategory(Enum):
    VIDEO = 'video'
    AUDIO = 'audio'
    PDF = 'pdf'


class ResponseEvent(Enum):
    SUBTITLE = 'subtitle'

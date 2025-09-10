
class InvalidYoutubeVideoUrlException(Exception):
       """
        This occurs when the youtube video url is in invalid format or the links from elsewhere.
       """

class VideoAlreadyAddedException(Exception):
       """
        This occurs when the youtube video which is being added does exist already in the database.
       """
       
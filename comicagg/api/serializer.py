import json
import time
from email import utils
from comicagg.comics.models import Comic, ComicHistory
from comicagg.comics.utils import UserOperations

class Serializer:
    """
    This class is used to serialize the data that has to be sent in the response to the API.
    Handles the output format, either JSON or XML, being JSON the default one.

    It works by building dictionaries and lists with the data and then convert these to JSON or XML.
    """
    def __init__(self, user=None, xml=False):
        """
        xml determines if the output is XML or JSON. By defaul it's JSON.
        """
        self.user = user
        self.prefer_xml = xml

    def serialize(self, object_to_serialize=None, last_strip=False, unread_strips=False, identifier=None):
        """
        Pass an instance of Comic, ComicHistory, a list of Comic instances or a dictionary to get a serialized version.
        If object_to_serialize is a list or a dict, then identifier will be used as the container name.
        """
        # TODO: Change the serializer to allow to return a list of integers
        d = dict()
        # Serialize a Comic object
        if isinstance(object_to_serialize, Comic):
            d["comic"] = self.build_comic_dict(object_to_serialize, last_strip, unread_strips)
        # Serialize a ComicHistory object (strip)
        elif isinstance(object_to_serialize, ComicHistory):
            d["strip"] = self.build_comichistory_dict(object_to_serialize)
        # Serialize a list of Comic objects using identifier as the parent element
        elif isinstance(object_to_serialize, list) and identifier:
            d[identifier] = [self.build_comic_dict(x, last_strip, unread_strips) for x in object_to_serialize]
        # Serialize a dictionary of objects using identifier as the parent element
        elif isinstance(object_to_serialize, dict) and identifier:
            d[identifier] = object_to_serialize
        # Serialize the current user information if there is no object_to_serialize
        elif not object_to_serialize and self.user:
            d["user"] = self.build_user_dict()
        else:
            raise ValueError("Object to serialize is not valid. Are you missing a parameter (identifier)?")

        if not self.prefer_xml:
            return json.dumps(d, separators=(',', ':'))
        return build_xml(d)

    def build_comic_dict(self, comic, last_strip=False, unread_strips=False):
        if type(comic) is not Comic:
            raise ValueError("This is not a comic")
        if not self.user:
            raise ValueError("To serialize a comic you need a user")
        user_operations = UserOperations(self.user)
        out = dict()
        if self.prefer_xml:
            out["__class"] = "comic"
        out["id"] = comic.id
        out["name"] = comic.name
        out["website"] = comic.website
        out["votes"] = comic.votes
        out["rating"] = comic.get_rating()
        out["added"] = str(user_operations.is_subscribed(comic))
        out["ended"] = str(comic.ended)
        out["unreadcount"] = user_operations.unread_comic_strips_count(comic)
        if last_strip:
            try:
                out["last_strip"] = self.build_comichistory_dict(comic.comichistory_set.all()[0])
            except:
                pass
        if unread_strips:
            out["unreads"] = [self.build_comichistory_dict(h) for h in user_operations.unread_comic_strips(comic)]
        return out

    def build_comichistory_dict(self, history):
        out = dict()
        if self.prefer_xml:
            out["__class"] = "strip"
        out["id"] = history.id
        out["imageurl"] = history.image_url()
        out["imagetext"] = history.alt_text if history.alt_text else ""
        out["date"] = datetime_to_rfc2822(history.date)
        out["timestamp"] = datetime_to_timestamp(history.date)
        return out

    def build_user_dict(self):
        user_operations = UserOperations(self.user)
        out = dict()
        if self.prefer_xml:
            out["__class"] = "user"
        out["username"] = self.user.username
        out["email"] = self.user.email
        out["totalcomics"] = len(user_operations.all_comics())
        out["unreadcomics"] = len(user_operations.unread_comics())
        # TODO: Return also the number of new comics
        return out

# Helper functions

def build_xml(what):
    """
    what should be a dictionary with only one key which will be the root element
    """
    if len(what.keys()) != 1:
        raise ValueError("The base Dictionary can only contain one item")
    out = '<?xml version="1.0" encoding="UTF-8" ?>\r\n'
    for k, v in what.items():
        out += build_xml_element(k, v)
    return out

def build_xml_element(name, value):
    """
    Builds a XML element whose tag is name and the content is value. Value will be parsed to XML accordingly.
    """
    # If the value passed is a list, then we need just to create opening and closing tags using name and recurse
    if type(value) is list:
        out = "<%s>%s</%s>" % (
            name,
            ''.join([build_xml_element(None, x) for x in value]),
            name)
    # If value is dict, then parse all values
    else:
        attx = dict()
        child = None
        for k, v in value.items():
            # If any value is a dict or list, then this element will need opening and closing tags
            if type(v) is dict:
                child = build_xml_element(v["__class"], v)
            elif type(v) is list:
                # NOTE: If lists should not be wrapped inside an element
                # child = ''.join([build_xml_element(None, x) for x in v])
                child = build_xml_element(k, v)
            else:
                # While parsing the values, build a dict with the values that are scalar as they'll be attributes
                attx[k] = v

        tag = name if name else attx["__class"]
        out = "<" + tag
        if len(attx):
            out += " "
            out += " ".join(['%s="%s"' % (k, v) for k, v in attx.items() if not k.startswith("__")])
        if child:
            out += ">" + child + "</" + tag + ">"
        else:
            out += "/>"
    return out

def datetime_to_timestamp(dt):
    tup = dt.timetuple()
    return time.mktime(tup)

def datetime_to_rfc2822(dt):
    return utils.formatdate(datetime_to_timestamp(dt))

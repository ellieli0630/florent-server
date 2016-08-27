# -*- coding: utf-8 -*-
import yelp

from config import yelp_API_key  # , yelp_categories

yelp_api = yelp.Api(**yelp_API_key)


def get_places(location, query=None, radius=3000, limit=10, offset=0, type1=None):
    """
    Get popular places near user.

    Args:
        location: user location (<str>)
        query: place to visit (<str>)
        radius: search radius in meters, default 3km (<int>)
        limit: number of places to show, max 20, default 10 (<int>)
        offset: offset the list of returned placed by this amount, default 0 (<int>)
        type1: place category, if more than one category separate them by comma ("coffee,parking") (<str>)

    Returns: list of dictionaries with place name, rating, etc. (<list>)
    """
    # print "GET PLACES"
    args = {"location": location,
            "term": query,
            "limit": limit,
            "radius_filter": radius,
            "offset": offset,
            "sort": 2}
    # print args

    if type1 is not None:
        args["category_filter"] = type1

    response = ""
    places = yelp_api.Search(**args)

    for place in places.businesses:
        resp = dict()

        resp["name"] = place.name
        # print "type1 "+str(type(resp["name"]))
        rating = unicode(place.rating)
        resp["rating"] = rating
        # print "type 1111"+str(type(resp["rating"]))
        # resp["review count"] = place.review_count

        # resp["phone"] = place.phone

        resp["phone"] = place.display_phone
        # print "type2 "+str(type(resp["phone"]))
        # resp["img"] = place.image_url

        resp["city"] = place.location.city
        # print "type3 "+str(type(resp["city"]))

        r = place.location.display_address
        address = ",".join(r)
        resp["address"] = address
        resp["mobile_url"] = place.mobile_url
        resp["snippet_text"] = place.snippet_text
        # print "type4"+str(type(resp["address"]))
        # print "type5"+str(type(resp["mobile_url"]))
        # print "type6"+str(type(resp["snippet_text"]))
        # resp["coordinates"] = place.location.coordinate

        # resp["neighborhoods"] = place.location.neighborhoods

        # for key, val in resp.iteritems():
        #     print "key, val"
        #     print key, val
        #     print "-----------"
        #
        #     response += (key) + ": " + (val) + " "

        response += ", ".join([place.name,
                               rating + " stars",
                               "Yelp highlights: " + place.snippet_text[:97] + "..."])
        response += " Address: " + address
        response += "\n"
    # print "TYPE "
    # print "resp: "
    # response=response.decode("utf-8")
    response=response.encode("ascii", "ignore")
    # print type(response)
    return response


if __name__ == "__main__":
    print "popular places near user"
    result = get_places(location="Arlington Heights, LA", type1="coffee,parking")
    print result
    # for i in result:
    #     print i

    print "places by user query"
    result = get_places(location="1st street NY", query="cafes", limit=3)
    print result
    # print "places by user query"
    # result = get_places(location="1st street NY", query="cafes", offset=3, limit=3)
    # print result
    # for i in result:
    #     print i

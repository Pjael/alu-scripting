#!/usr/bin/python3
"""Module that recursively queries the Reddit API for all hot post titles."""
import json
import urllib.error
import urllib.request


class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Redirect handler that blocks all HTTP redirects."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        """Return None to prevent following any redirect."""
        return None


def recurse(subreddit, hot_list=[], after="", first_call=True):
    """Recursively collect all hot post titles for a given subreddit.

    Args:
        subreddit (str): the name of the subreddit to query.
        hot_list (list): accumulator list of post titles collected so far.
        after (str): pagination token for the next page of results.
        first_call (bool): whether this is the initial call, used to
            reset the accumulator so results don't leak between calls.

    Returns:
        list: all hot post titles for the subreddit, or None if the
            subreddit is invalid or has no results.
    """
    if first_call:
        hot_list = []

    url = "https://www.reddit.com/r/{}/hot.json?limit=100".format(subreddit)
    if after:
        url += "&after={}".format(after)
    headers = {"User-Agent": "Mozilla/5.0 (recurse-hot-list:v1.0)"}

    request = urllib.request.Request(url, headers=headers)
    opener = urllib.request.build_opener(NoRedirectHandler)

    try:
        with opener.open(request) as response:
            if response.status != 200:
                return None
            data = json.loads(response.read().decode())
    except (urllib.error.HTTPError, urllib.error.URLError):
        return None

    posts = data.get("data", {}).get("children", [])
    if not posts and first_call:
        return None

    for post in posts:
        hot_list.append(post.get("data", {}).get("title"))

    next_after = data.get("data", {}).get("after")
    if next_after:
        return recurse(subreddit, hot_list, next_after, False)

    return hot_list

#!/usr/bin/python3
"""Module that queries the Reddit API for a subreddit's top 10 hot posts."""
import json
import urllib.error
import urllib.request


class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Redirect handler that blocks all HTTP redirects."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        """Return None to prevent following any redirect."""
        return None


def top_ten(subreddit):
    """Print the titles of the first 10 hot posts for a given subreddit.

    Args:
        subreddit (str): the name of the subreddit to query.

    Prints:
        The title of each of the first 10 hot posts, one per line.
        None, if the subreddit is invalid.
    """
    url = "https://www.reddit.com/r/{}/hot.json?limit=10".format(subreddit)
    headers = {"User-Agent": "Mozilla/5.0 (top-ten-counter:v1.0)"}

    request = urllib.request.Request(url, headers=headers)
    opener = urllib.request.build_opener(NoRedirectHandler)

    try:
        with opener.open(request) as response:
            if response.status != 200:
                print(None)
                return
            data = json.loads(response.read().decode())
    except (urllib.error.HTTPError, urllib.error.URLError):
        print(None)
        return

    posts = data.get("data", {}).get("children", [])
    if not posts:
        print(None)
        return

    for post in posts:
        print(post.get("data", {}).get("title"))

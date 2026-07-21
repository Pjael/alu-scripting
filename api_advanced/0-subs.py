#!/usr/bin/python3
"""Module that queries the Reddit API for a subreddit's subscriber count."""
import json
import urllib.error
import urllib.request


class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Redirect handler that blocks all HTTP redirects."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        """Return None to prevent following any redirect."""
        return None


def number_of_subscribers(subreddit):
    """Return the number of subscribers for a given subreddit.

    Args:
        subreddit (str): the name of the subreddit to query.

    Returns:
        int: the number of subscribers, or 0 if the subreddit is invalid.
    """
    url = "https://www.reddit.com/r/{}/about.json".format(subreddit)
    headers = {"User-Agent": "Mozilla/5.0 (subscriber-counter:v1.0)"}

    request = urllib.request.Request(url, headers=headers)
    opener = urllib.request.build_opener(NoRedirectHandler)

    try:
        with opener.open(request) as response:
            if response.status != 200:
                return 0
            data = json.loads(response.read().decode())
    except (urllib.error.HTTPError, urllib.error.URLError):
        return 0

    return data.get("data", {}).get("subscribers", 0)

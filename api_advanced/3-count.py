#!/usr/bin/python3
"""Module that recursively queries the Reddit API to count keywords."""
import json
import urllib.error
import urllib.request


class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Redirect handler that blocks all HTTP redirects."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        """Return None to prevent following any redirect."""
        return None


def count_words(subreddit, word_list, word_count=None, after="",
                 first_call=True):
    """Recursively count keyword occurrences in a subreddit's hot titles.

    Args:
        subreddit (str): the name of the subreddit to query.
        word_list (list): the keywords to search for and count.
        word_count (dict): accumulator dict mapping lowercase keyword
            to running occurrence count.
        after (str): pagination token for the next page of results.
        first_call (bool): whether this is the initial call, used to
            reset the accumulator and normalize word_list once.

    Prints:
        Each matched keyword and its count, sorted by count descending
        then alphabetically ascending. Prints nothing if the subreddit
        is invalid or no keywords match.
    """
    if first_call:
        word_count = {}
        normalized = [word.lower() for word in word_list]
        for word in normalized:
            word_count[word] = word_count.get(word, 0)
        word_list = normalized

    url = "https://www.reddit.com/r/{}/hot.json?limit=100".format(subreddit)
    if after:
        url += "&after={}".format(after)
    headers = {"User-Agent": "Mozilla/5.0 (count-words:v1.0)"}

    request = urllib.request.Request(url, headers=headers)
    opener = urllib.request.build_opener(NoRedirectHandler)

    try:
        with opener.open(request) as response:
            if response.status != 200:
                return
            data = json.loads(response.read().decode())
    except (urllib.error.HTTPError, urllib.error.URLError):
        return

    posts = data.get("data", {}).get("children", [])
    if not posts and first_call:
        return

    for post in posts:
        title = post.get("data", {}).get("title", "")
        for token in title.split():
            token = token.lower()
            if token in word_list:
                word_count[token] = word_count.get(token, 0) + 1

    next_after = data.get("data", {}).get("after")
    if next_after:
        return count_words(subreddit, word_list, word_count,
                            next_after, False)

    matches = [(word, count) for word, count in word_count.items()
               if count > 0]
    matches.sort(key=lambda pair: (-pair[1], pair[0]))
    for word, count in matches:
        print("{}: {}".format(word, count))

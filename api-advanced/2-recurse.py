#!/usr/bin/python3

#!/usr/bin/python3
"""
This module defines a recursive function to query the Reddit API and
return a list containing the titles of all hot articles for a given subreddit.
"""

import requests


def recurse(subreddit, hot_list=None, after=None):
    """
    Recursively queries the Reddit API and returns a list of titles of all
    hot articles for a given subreddit.

    Args:
        subreddit (str): The name of the subreddit.
        hot_list (list): List to accumulate titles (used for recursion).
        after (str): Token for the next page of results.

    Returns:
        list: List of titles of all hot articles, or None if no results.
    """
    if hot_list is None:
        hot_list = []

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {"User-Agent": "python:recurse:v1.0 (by /u/yourusername)"}
    params = {"after": after, "limit": 100}

    try:
        response = requests.get(
            url, headers=headers, params=params, allow_redirects=False, timeout=10
        )
        if response.status_code != 200:
            return None
        data = response.json().get("data", {})
        posts = data.get("children", [])
        for post in posts:
            hot_list.append(post.get("data", {}).get("title"))
        after = data.get("after")
        if after:
            return recurse(subreddit, hot_list, after)
        return hot_list if hot_list else None
    except Exception:
        return None

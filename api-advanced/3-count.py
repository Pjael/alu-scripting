#!/usr/bin/python3

#!/usr/bin/python3
"""
This module defines a recursive function to query the Reddit API,
parse the titles of all hot articles, and print a sorted count of
given keywords (case-insensitive, delimited by spaces).
"""

import requests


def count_words(subreddit, word_list, hot_list=None, after=None, counts=None):
    """
    Recursively queries the Reddit API, parses the titles of all hot articles,
    and prints a sorted count of given keywords (case-insensitive).

    Args:
        subreddit (str): The name of the subreddit.
        word_list (list): List of keywords to count.
        hot_list (list): List to accumulate titles (used for recursion).
        after (str): Token for the next page of results.
        counts (dict): Dictionary to accumulate keyword counts.

    Prints:
        Sorted count of keywords found in the titles.
    """
    if hot_list is None:
        hot_list = []
    if counts is None:
        counts = {}

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {"User-Agent": "python:count.words:v1.0 (by /u/yourusername)"}
    params = {"after": after, "limit": 100}

    try:
        response = requests.get(
            url, headers=headers, params=params, allow_redirects=False, timeout=10
        )
        if response.status_code != 200:
            return

        data = response.json().get("data", {})
        posts = data.get("children", [])
        for post in posts:
            title = post.get("data", {}).get("title", "")
            hot_list.append(title)

        after = data.get("after")
        if after:
            count_words(subreddit, word_list, hot_list, after, counts)
        else:
            # Prepare word count
            word_map = {}
            for word in word_list:
                key = word.lower()
                word_map[key] = word_map.get(key, 0) + 1  # handle duplicates

            for title in hot_list:
                words = title.lower().split()
                for key in word_map:
                    # Count only exact matches (not substrings)
                    count = words.count(key)
                    if count > 0:
                        counts[key] = counts.get(key, 0) + count

            # Multiply by number of times word appears in word_list
            for key in counts:
                counts[key] *= word_map[key]

            # Filter out zero counts and sort
            sorted_counts = sorted(
                [(k, v) for k, v in counts.items() if v > 0],
                key=lambda x: (-x[1], x[0])
            )

            for word, count in sorted_counts:
                print(f"{word}: {count}")

    except Exception:
        return

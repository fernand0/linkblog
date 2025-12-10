#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This script generates a Markdown list of links published on Twitter for a given date,
using the data from the publication cache.
"""

import sys
import os
from datetime import datetime
from socialModules.modulePublicationCache import PublicationCache

def get_twitter_links_by_date(date_str):
    """
    Retrieves Twitter links for a specific date from the publication cache.

    Args:
        date_str (str): The date in 'YYYY-MM-DD' format.

    Returns:
        list: A list of dictionaries, each containing the 'title' and 'original_link'
              of a Twitter publication for the given date.
    """
    try:
        # Validate the date format
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        print("Error: Invalid date format. Please use 'YYYY-MM-DD'.")
        return []

    # Initialize the publication cache
    cache = PublicationCache()
    
    # Get all publications from Twitter
    twitter_publications = cache.get_publications_by_service('twitter')

    # Filter publications by the selected date
    links_for_date = []
    for pub in twitter_publications:
        pub_date_str = pub.get('publication_date', '').split('T')[0]
        try:
            pub_date = datetime.strptime(pub_date_str, '%Y-%m-%d').date()
            if pub_date == selected_date:
                links_for_date.append({
                    'title': pub.get('title', 'No Title'),
                    'original_link': pub.get('original_link', '#')
                })
        except (ValueError, TypeError):
            # Ignore publications with invalid date formats
            continue
            
    return links_for_date

def create_jekyll_post(date_str):
    """
    Creates a Jekyll post with the Twitter links for the specified date.

    Args:
        date_str (str): The date in 'YYYY-MM-DD' format.
    """
    # Get the links for the specified date
    twitter_links = get_twitter_links_by_date(date_str)
    
    if not twitter_links:
        print(f"No Twitter links found for {date_str}. No post created.")
        return

    # Generate the Markdown list of links
    markdown_output = ""
    for link in twitter_links:
        markdown_output += f"- [{link['title'].replace('|', '\|')}]({link['original_link']})\n"

    # Define post details
    post_title = f"Links for {date_str}"
    post_filename = f"{date_str}-twitter-links.md"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    post_filepath = os.path.join(script_dir, '..', '_posts', post_filename)

    # Create the full post content with Jekyll front matter
    post_content = f"""---
layout: post
title: "{post_title}"
date: {date_str}
---

{markdown_output}
"""

    # Write the content to the post file
    try:
        with open(post_filepath, "w", encoding="utf-8") as f:
            f.write(post_content)
        print(f"Successfully created Jekyll post: {post_filepath}")
    except IOError as e:
        print(f"Error creating post file: {e}")

def main():
    """
    Main function to execute the script.
    It expects a date as a command-line argument.
    """
    if len(sys.argv) != 2:
        print("Usage: python list_twitter_links_by_date.py YYYY-MM-DD")
        sys.exit(1)

    date_str = sys.argv[1]
    create_jekyll_post(date_str)

if __name__ == "__main__":
    main()

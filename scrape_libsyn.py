"""
Reads RSS feeds (prototypically from libsyn) and downloads metadata and
audio files as mp3s.
"""

import csv
import os
import re
import shutil
import feedparser
import requests

def download_libsyn(url):
    """ Process a single libsyn feed."""

    print("Requesting URL %s" % url)
    data = requests.get(url).text
    parsed_rss = feedparser.parse(data)
    podcast_title = parsed_rss["feed"]["title"]
    print("RSS feed read, extracted title %s" % podcast_title)

    if not os.path.isdir("./shows/%s" % podcast_title):
        try:
            os.makedirs("./shows/%s/episodes" % podcast_title, exist_ok = True)
        except:
            print("Fatal error making containing folder")
            return 1

    with open("./shows/%s/feed.rss" % podcast_title, "w") as f:
        f.write(data)

    with open("./shows/%s/url.txt" % podcast_title, "w") as f:
        f.write("%s\n" % url)

    print(("%s entries detected in RSS feed, extracting URLs" %
          len(parsed_rss.entries)))
    episodes = [[parse_link(x.links), parse_file_out(x.title)]
                for x in parsed_rss.entries]
    with open("./shows/%s/download_urls.csv" % podcast_title, "w") as f:
        write_csv = csv.writer(f)
        write_csv.writerow(["URL", "out_filename"])
        for row in episodes:
            write_csv.writerow(row)

    print("Now proceeding to download MP3s.")
    for index, row in enumerate(episodes):
        print("  Downloading episode %s/%s: %s" %
              (index, len(episodes), row[1]))
        download_episode(podcast_title, row)

    return 0

def download_episode(podcast_title, row):
    """ Downloads a single episode. """
    if os.path.isfile("./shows/%s/episodes/%s" % (podcast_title, row[1])):
        print("  %s already downloaded, skipping..." % row[1])
        return

    data = requests.get(row[0], stream=True)
    with open("./shows/%s/episodes/%s" % (podcast_title, row[1]), "wb") as out_file:
        data.raw.decode_content = True
        shutil.copyfileobj(data.raw, out_file)

def parse_file_out(title):
    """ Extract an episode filename from the episode title. """
    match = re.search("Episode ([0-9]{1,4})", title, re.IGNORECASE)
    if match:
        file_out = "%s - %s.mp3" % (match.group(1), title)
    else:
        file_out = "%s.mp3" % title

    file_out = re.sub(r"[^a-zA-Z0-9 \-\.]", "", file_out)
    return file_out

def parse_link(links):
    """ Podcasts might have multiple links per episode, we want the mp3. """
    return next((x["url"] for x in links if ".mp3" in x["url"]), None)

def process_all_urls(feed_list):
    """ Iterate over several feeds. """
    feed_urls = [x.strip() for x in open(feed_list, "r").readlines()]
    print("%s feeds to scrape..." % len(feed_urls))
    for feed_url in feed_urls:
        download_libsyn(feed_url)

if __name__ == "__main__":
    process_all_urls("feeds.txt")

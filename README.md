# podcast_scraper

Scrapes full podcast RSS feeds.

# Configuring input

Edit `feeds.txt`, one URL per line. Blank lines are ignored. In general any well-formed podcast RSS feed should ingest; note that websites which are not podcast RSS feeds will not work.

# Output files

The script will place all results in a folder named `shows/` (creating the folder if necessary). Within this folder, each show will have a folder reflecting the show's name. Inside that folder, the following format applies:

* `url.txt`: A text file containing the URL from feeds.txt that was read.
* `feed.rss`: The raw feed downloaded with no modifications
* `download_urls.csv`: A two-column CSV containing the columns `URL` (the URL of the mp3 being downloaded) and `out_filename` (the local filename of the episode downloaded)
* `episodes/`: A folder containing each episode as a single MP3.

The default filename is a santized format of the episode metadata title. If the title contains "Episode <XXX>", the episode number is extracted and the file name format is `<XXX> - Episode Title.mp3`. If no episode number is extracted, then the file name format is `Episode Title.mp3`

# Requirements

The script requires python3 and the external libraries `requests` and `feedparser`. I will update later with a format requirements.txt.

## Download and Change Wallpaper from Bing in Ubuntu ##

A simple, sometimes naive python script for downloading wallpapers from bing.com, maintain them, and set one of them as the wallpaper.

Work together with crontab to do daily download and a 10-minute-frequency wallpaper change.

### Environment ###

* Python 2.7

* Dependencies: python-requests

* Tested only on Ubuntu 14.04

### Usage ###

1. Clone this repo to your `~/Pictures/`

2. Using `crontab -e` to edit your user's cron config. Add the two schedules in `wallpaper-cron` into your cron config.

### Miscellaneous ###

See `handle_wallpaper.py` for details. 

Default working directory is "~/Pictures/bing-wallpaper". Change it in code if needed. 

`MAX_IMAGE_NUMBER` default equals 7 because response from bing.com only contains 8 entries. 

`BING_GALLERY_URL` can be modified to other markets. 

Alternatives and valid values for market: [Bing Picture of the Day as Desktop Wallpaper?](http://askubuntu.com/questions/379377/bing-picture-of-the-day-as-desktop-wallpaper)

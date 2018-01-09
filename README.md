# OneOffs

A collection of simple files i've created for various purposes. Most are exploritory/proof of concept style items

## Descriptions
#### BostonReaderLambda.py:

This file is the code hosted on an AWS Lambda function to support a basic alexa skill, which reads the top headlines from the boston subreddit

#### CrawlForPngs.py:
This is a simple script that crawls through a file looking for file paths to pngs, and replaces that filepath. Used to refactor hadrcoded filepaths in source code to a method call

#### Add_Track.py && myauth.py
These scripts were part of a system to add the currently playing song on spotify to a playlist. Add_track.py uses the spotify web api to accomplish this, which requires authentication. myauth.py handles the one-time authorization by running a simple Bottle server to listen for the auth services callback

Requires:
  - Bottle
  - Spotipy

#!/usr/bin/env python
# Author: Gary Hooks
# Email: garyhooks@gmail.com
# Publish Date: 4th April 2019
# Licence: GNU GPL

# Ensure tweepy is installed as Python3 Library
import tweepy
import os
import time
import datetime

# Set up base path - ensures this works in Linux/Windows environments
BASE_PATH = os.sys.path[0]

# Sleep Timer - WARNING: this prevents a RateLimitError, so be careful changing it (unit = seconds)
SLEEP_TIMER = 5*60

# A small amount of sleep after each deletion ...
SMALL_SLEEP = 0.5

# Age of tweet - default: all tweets older than 7 days
AGE_OF_TWEET = 7

# These are keys for the development API and are static
consumer_key = "<enter your key>"
consumer_secret = "<enter your secret>"

def get_statuses(api, username, target_username, friend_dump_file):

    # Make a "nice" output for user
    print("\n")
    print("Deleting Tweets for user: " + target_username)
    print("All tweets older than " + str(AGE_OF_TWEET) + " days will be deleted")
    print("---------------------------------------------------------------------------\n")

    try:

        ## use tweepy.cursor to obtain the target user list
        ## for look to circulate through them

        deleted = 0

        for get_statuses in tweepy.Cursor(api.user_timeline, screen_name=target_username).pages():

            for status in get_statuses:

                try:

                    # Get API returned variables ready
                    tweet_id = status.id
                    tweet_text = (status.text).replace("\n", "")
                    tweet_creation_date = status.created_at

                    # Get the age of the tweet in days - e.g. return of "8" indicates it was 8 days ago
                    difference = get_days(tweet_creation_date)

                    # If the age of the tweet is greater than the pre-set variable (set at the top), then delete
                    if difference > AGE_OF_TWEET:
                        deleted += 1
                        print ("#" + str(deleted) + ": \t Deleting this tweet --> " + tweet_text)
                        api.destroy_status(tweet_id)

                        # Sleep just a tiny bit...
                        time.sleep(SMALL_SLEEP)
                except:
                    continue


        print("---------------------------------------------------------------------------")
        print("Process Finished")
        print("Total Tweets Deleted: " + str(deleted))

    except tweepy.RateLimitError:
        # If you hit a rate limit then sleep for a little bit... recommended is 5 minutes (5x60)
        print("Rate Limit Error: Sleeping for a little while")
        time.sleep(SLEEP_TIMER)


def get_days(created_date):

    # Get the current date and convert to string
    now = str(datetime.date.today())

    # Prepare it for comparison
    now_ready = datetime.datetime.strptime(now, "%Y-%m-%d")

    # Calculate the difference between the two days
    difference = now_ready - created_date

    # Return the single integer value of the days between the two days
    return difference.days

def main():

    ## First ask user what their Twitter username is
    username = input("Please Enter your Twitter username: ")

    ## Now create path variable for text file to store tokens
    token_file = BASE_PATH + "/" + username + " - tokens.txt"


    ## Ok, now check if the access Tokens for this user are available
    ## If not user should be asked to visit URN and authorise access via supplied PIN code
    if os.path.isfile(token_file):

        # Yes user is known to us... open the corresponding TOKEN_FILE
        with open(token_file, "r") as file:

            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.secure = True
            access_token = file.readline().strip()
            access_token_secret = file.readline().strip()

    else:

        # No user is not known ... ask them to visit URL and read in PIN code supplied by Twitter
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.secure = True
        auth_url = auth.get_authorization_url()
        print("Visit this URL and authorise the app to use your Twitter account: " + auth_url)
        verifier = input('Type in the generated PIN: ').strip()

        # We have the tokens - now save them into respective variables
        auth.get_access_token(verifier)
        access_token = auth.access_token
        access_token_secret = auth.access_token_secret

        # Save them into TOKEN_FILE for future use
        with open(token_file, "w") as f:
            f.write(access_token + "\n")
            f.write(access_token_secret)

        f.close()

    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    target_username = input("Enter target username, to delete statuses older than " + str(AGE_OF_TWEET) + " days: ")
    statuses_file = BASE_PATH + "/" + target_username + "_statuses.txt"

    # Call Function
    get_statuses(api, username, target_username, statuses_file)


if __name__ == "__main__":
    main()

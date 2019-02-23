#!/usr/bin/env python
# Author: Gary Hooks
# Email: garyhooks@gmail.com
# Publish Date: 7th August 2017
# Licence: GNU GPL
#
# Usage: python3 ./auto_follow.py

# Ensure tweepy is installed as Python3 Library
import tweepy
import os
import time

# Set up base path - ensures this works in Linux/Windows environments
BASE_PATH = os.sys.path[0]

# Sleep Timer - WARNING: this prevents a RateLimitError, so be careful changing it (unit = seconds)
SLEEP_TIMER = 30

# These are keys for the development API and are static
consumer_key = "fssPhvXzLwmZL4shqnA7GvGLT"
consumer_secret = "C0DIDjp1sERxmcuJSkFc98l3GF7PtB7ObER6JW4Smrv5rLXkSx"

def auto_follow(api, new_user_file):

    # Make a "nice" output for user
    print("\n")
    print("Follow requests sent to the following users: ")
    print("---------------------------------------------------------------------------\n")

    # Start Counter
    friends = 0

    # open the new user file list and begin reading
    with open(new_user_file, "r") as f:

        # For each friend, use api to create_friendship and then print output
        # Sleep for specified time to avoid hitting RateLimitError
        for friend in f.readlines():
            friends += 1
            api.create_friendship(friend)
            print (str(friends) + ") " + friend.strip())
            time.sleep(SLEEP_TIMER)

    # Function End
    return 0


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

    new_user_file = input("Enter filename of new usernames to target: ")


    # Call Function
    auto_follow(api, new_user_file)

    print("---------------------------------------------------------------------------")
    print("Process Finished")


if __name__ == "__main__":
    main()

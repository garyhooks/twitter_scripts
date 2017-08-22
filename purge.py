#!/usr/bin/env python
# Author: Gary Hooks
# Web: http://www.garyhooks.co.uk
# Email: garyhooks@gmail.com
# Publish Date: 7th August 2017
# Licence: GNU GPL

# Ensure tweepy is installed as Python3 Library
import tweepy
import os
import time
import sys
import json

# Set up base path - ensures this works in Linux/Windows environments
BASE_PATH = os.sys.path[0]

# Sleep Timer - WARNING: this prevents a RateLimitError, so be careful changing it (unit = seconds)
SLEEP_TIMER = 10

# These are minimum values so that we avoid listing spam accounts, or inactive users
# Also maximum value is to avoid listing accounts with 100k + followers
MIN_TWEETS = 500
MIN_FOLLOWERS = 200
MAX_FOLLOWERS = 2000
MIN_FRIENDS = 200


# These are keys for the development API and are static
consumer_key = "fssPhvXzLwmZL4shqnA7GvGLT"
consumer_secret = "C0DIDjp1sERxmcuJSkFc98l3GF7PtB7ObER6JW4Smrv5rLXkSx"

def purge(api, username):

    # Make a "nice" output for user
    print("\n")
    print("Searching users and unfollowing one-way relationships of : " + username)
    print("---------------------------------------------------------------------------------\n")

    counter = 0

    try:

        ## use tweepy.cursor to obtain the target user list
        ## for look to circulate through them

        for friend in tweepy.Cursor(api.friends).items():
            # Process the friend here

            friendship = api.show_friendship(source_screen_name = username, target_screen_name = friend.screen_name)

            for information in friendship:
                following_me = information.following

            if following_me is False:
                print (friend.screen_name + " - They aren't following me......... GOODBYE")
                api.destroy_friendship(friend.screen_name)

            time.sleep(5)

        for friends in tweepy.Cursor(api.followers).pages():

            ## for each friend found...  save their screen name to specified file dump

            for friend in friends:

                screen_name = friend.screen_name



                friendships = api.show_friendship(target_screen_name = screen_name)
                result = json.loads(api.show_friendship(source_screen_name=username, target_screen_name=screen_name))[0][0][2]
                print(result)
                sys.exit()


                with open(friend_dump_file, "a") as f:

                    counter += 1
                    f.write(screen_name + "\n")
                    f.close()

                    print (str(counter) + ") " + screen_name + " found and saved to file")

                    time.sleep(SLEEP_TIMER)





    except tweepy.RateLimitError:
        print("Rate Limit Error: Sleeping for 60 seconds...")
        time.sleep(60)


    print ("\n\n")
    print("---------------------------------------------------------------------------")
    print("Process Finished")


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

    purge(api, username)


if __name__ == "__main__":
    main()

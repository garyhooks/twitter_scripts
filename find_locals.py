#!/usr/bin/env python
# Author: Gary Hooks
# Email: garyhooks@gmail.com
# Publish Date: 7th August 2017
# Licence: GNU GPL
#
# Usage: python3 ./find_locals.py

# Ensure tweepy is installed as Python3 Library
import tweepy
import os
import time
import re

# Set up base path - ensures this works in Linux/Windows environments
BASE_PATH = os.sys.path[0]

# Sleep Timer - WARNING: this prevents a RateLimitError, so be careful changing it (unit = seconds)
SLEEP_TIMER = 10

# These are keys for the development API and are static
consumer_key = "fssPhvXzLwmZL4shqnA7GvGLT"
consumer_secret = "C0DIDjp1sERxmcuJSkFc98l3GF7PtB7ObER6JW4Smrv5rLXkSx"

def find_friends(api, username, target_username, friend_dump_file, location):

    # Make a "nice" output for user
    print("\n")
    print("Saving the names of users in specified location who are following: " + target_username)
    print("--------------------------------------------------------------------------------------------------\n")

    # Counter to track how many total users read and considered
    counter = 0

    # Matched to track how many are 100% matches and can be added to file
    matched = 0

    try:

        ## use tweepy.cursor to obtain the target user list
        ## for look to circulate through them

        for friends in tweepy.Cursor(api.friends, id=target_username).pages():

            ## for each friend found...

            for friend in friends:

                ## Check their location to ensure
                screen_name = friend.screen_name
                friend_location = friend.location.lower()
                counter += 1

                ## Ensure the potential new user is not the user themselves!
                if screen_name != username:

                    # change location entered by user to lowercase ... and check if potential user's location is a match
                    regexp = re.compile(location.lower())
                    if regexp.search(friend_location) is not None:

                        # This is a matched user at this point... increase variable and add the filaname to a file
                        matched += 1
                        print("User: " + screen_name + " is a match ... writing to file - " + str(matched) + " .... total users read: " + str(counter))

                        with open(friend_dump_file, "a") as f:
                            f.write(screen_name + "\n")
                            f.close()

                time.sleep(SLEEP_TIMER) #sleep for 10 seconds to stop a RateLimitError

    except tweepy.RateLimitError:
        print("Rate Limit Error: Sleeping for 60 seconds...")
        time.sleep(60)




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

    target_username = input("Enter target username, to save their users: ")
    friend_dump_file = BASE_PATH + "/" + target_username + "_local_followers.txt"

    location = input("Please enter the place name of users you want to target (e.g. London): ")

    # Call Function
    find_friends(api, username, target_username, friend_dump_file, location)

if __name__ == "__main__":
    main()

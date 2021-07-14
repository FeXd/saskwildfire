# TWEEPY DOCUMENTATION - https://docs.tweepy.org/en/latest/
# AUTHENTICATION TUTORIAL - https://docs.tweepy.org/en/latest/auth_tutorial.html
import tweepy

# YOU MUST HAVE A TWITTER DEVELOPER ACCOUNT TO USE
# https://developer.twitter.com/en/apply-for-access
# All new developers must apply for a developer account to access the Twitter developer platform.
# Once approved, you can begin to use our new Twitter API v2, or our v1.1 standard and premium APIs.

# CONSUMER KEYS - available under Projects & Apps > Standalone Apps > Your App > Keys and tokens
# Do not commit the tokens to git. These should also be copied to the .env file
consumer_key = ''
consumer_secret = ''

# AUTHENTICATE WITH TWITTER
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

# STEP 1 - GET OAUTH TOKENS - enable if we need to get OAuth tokens
if False:
    # Get the URL that we need to visit
    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        print('Error! Failed to get request token.')

    # Token for convenience
    request_token = auth.request_token['oauth_token']

    # Print out both and exit - copy paste them appropriately below and disable

    print(redirect_url)
    print(request_token)

    # Should look something like:
    # https://api.twitter.com/oauth/authorize?oauth_token=ABC123
    # ABC123

    # Next, manually visit the redirect_url page and authorize for desired twitter account
    # After authorizing your app, you can get your oauth_verifier from your address bar
    # Should look something like:
    # https://website.com/?oauth_token=ABC123&oauth_verifier=XYZ987

    exit()

verifier = 'XYZ987'
request_token = {'oauth_token': 'ABC123', 'oauth_token_secret': verifier}

# STEP 2 - GET OAUTH TOKENS - enable after completing step 1
if False:
    auth.request_token = request_token
    try:
        auth.get_access_token(verifier)
    except tweepy.TweepError:
        print('Error! Failed to get access token.')

    # Print out access_token and access_token_secret

    print('access_token', auth.access_token)
    print('access_token_secret', auth.access_token_secret)

    # Copy the access_token and access_token_secret and place in the .env file

    exit()

# YOU ARE DONE - You should be able to run main.py successfully
# Feel free to past tokens below, disable STEP 1 and STEP 2 and play with Tweepy API below
# API v1.1 Reference: https://docs.tweepy.org/en/latest/api.html
access_token = ''
access_token_secret = ''
auth.set_access_token(access_token, access_token_secret)

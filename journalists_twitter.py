# %%
import json
import tweepy
from pprint import pprint
import tqdm

# %%
CONSUMER_KEY = "SL5KvNaqmVjJ4XsibIpLxLYLu"
CONSUMER_KEY_SECRET = "3AkUPywCQeST2QeJu7IogyFMUw99mmWjEifdY9kqxuyn57GnVv"
ACCESS_TOKEN = "1280981223829958657-PDDq8Ip6uBUuKUfroTAKUdfMgddk7W"
ACCESS_TOKEN_SECRET = "81CT1Vo4gb51KLvebIHUdyMPuKv5LhnaZUM7Siz7u9VJT"

# %%
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
redirect_url = auth.get_authorization_url()
print(redirect_url)

# %%
auth.get_access_token('0267618')

# %%
with open('journalists.json', 'r') as f:
    koo_users = json.load(f)

# %%
def search_user(name):
    res = api.search_users(q=name, tweet_mode='extended')
    if len(res) == 0:
        return None
    return res[0]


# %%
class User:
    def __init__(self, koo_user, twitter_user):
        self.koo_user = koo_user
        self.twitter_user = twitter_user

    def print(self):
        if self.twitter_user is None:
            return f"{self.koo_user['name']}\t{self.koo_user['userHandle']}\t\t\t{self.koo_user['followerCount']}\t{self.koo_user['badgeType']}\n"
        else:
            return f"{self.koo_user['name']}\t{self.koo_user['userHandle']}\t{self.twitter_user.name}\t{self.twitter_user.screen_name}\t{self.koo_user['followerCount']}\t{self.koo_user['badgeType']}\n"

    @classmethod
    def schema(cls):
        return "Koo Name\tKoo Handle\tTwitter Name\tTwitter Handle\t# Followers on Koo\tVerified on Koo\n"


# %%
users = []

# %%
for koo_user in tqdm.tqdm(koo_users):
    twitter_user = search_user(koo_user['name'])
    users.append(User(koo_user, twitter_user))

# %%
with open('journalists_twitter.json', 'w') as f:
    json.dump([u.twitter_user._json if u.twitter_user else None for u in users], f)

# %%
with open('journalists.tsv', 'w') as f:
    f.write(User.schema())
    for user in users:
        f.write(user.print())
# %%

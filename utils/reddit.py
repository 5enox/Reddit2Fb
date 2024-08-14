from getfromenv import YOUR_CLIENT_ID, YOUR_CLIENT_SECRET, YOUR_APP_NAME
import praw

reddit = praw.Reddit(
    client_id=YOUR_CLIENT_ID,
    client_secret=YOUR_CLIENT_SECRET,
    user_agent=YOUR_APP_NAME
)

subreddit = reddit.subreddit("python")
for post in subreddit.hot(limit=10):
    print(post.title)

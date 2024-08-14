import time
import json
import os
import requests
import facebook as fb
import praw
from getfromenv import YOUR_CLIENT_ID, YOUR_CLIENT_SECRET, USER_AGENT, FACEBOOK_ACCESS_TOKEN


def get_reddit_posts(subreddit_name, limit=10):
    reddit = praw.Reddit(
        client_id=YOUR_CLIENT_ID,
        client_secret=YOUR_CLIENT_SECRET,
        user_agent=USER_AGENT
    )

    subreddit = reddit.subreddit(subreddit_name)

    posts = []
    for post in subreddit.hot(limit=limit):
        if post.is_reddit_media_domain:
            if hasattr(post, 'preview'):
                image_url = post.preview['images'][0]['source']['url']
                posts.append({"title": post.title, "image_url": image_url})

        elif hasattr(post, 'is_gallery') and post.is_gallery:
            if hasattr(post, 'media_metadata'):
                for image_id in post.media_metadata:
                    image_url = post.media_metadata[image_id]['p'][0]['u']
                    posts.append({"title": post.title, "image_url": image_url})

        elif post.url.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            posts.append({"title": post.title, "image_url": post.url})

    return posts


def reddit_get_and_save_posts(subreddit_name, limit=10):
    posts = get_reddit_posts(subreddit_name, limit)
    save_posts(filename='posts.json', posts=posts)


def load_posts(filename):
    """Load posts from a specified JSON file."""
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                if 'posts' in data and isinstance(data['posts'], list):
                    return data
        except (json.JSONDecodeError, ValueError):
            pass
    return {"posts": []}


def save_posts(filename, posts):
    """Save posts to a specified JSON file."""
    with open(filename, 'w') as f:
        json.dump({"posts": posts}, f, indent=4)


def filter_new_posts(current_posts, old_posts):
    """Filter out new posts that are not in the old posts."""
    old_ids = {post['title'] for post in old_posts['posts']}
    new_unique_posts = [
        post for post in current_posts['posts'] if post['title'] not in old_ids]
    return new_unique_posts


def process_posts():
    current_posts = load_posts('posts.json')
    old_posts = load_posts('old_posts.json')

    new_posts = filter_new_posts(current_posts, old_posts)

    save_posts(filename='new_posts.json', posts=new_posts)

    old_posts['posts'].extend(new_posts)
    save_posts('old_posts.json', old_posts['posts'])


def facebook_post_in_group(file_name):
    graph = fb.GraphAPI(access_token=FACEBOOK_ACCESS_TOKEN)

    with open(file_name, 'r') as file:
        data = json.load(file)
        posts = data['posts']

        for post in posts:
            response = requests.get(post['image_url'], stream=True)
            if response.status_code == 200:
                with open('temp_image', 'wb') as img_file:
                    img_file.write(response.content)

                with open('temp_image', 'rb') as img_file:
                    graph.put_photo(image=img_file, message=post['title'])
                    print(f"Posted to Facebook: {post['title']}")
            else:
                print(f"Failed to download image for post: {post['title']}")


if __name__ == '__main__':
    while True:
        reddit_get_and_save_posts('ProgrammerHumor')
        process_posts()
        facebook_post_in_group(file_name='new_posts.json')
        time.sleep(3600)  # Wait for 1 hour before checking again

import time
import requests
import json
from instagrapi import Client

# Initialize the client
client = Client()

# Login to Instagram
client.login(username="omen.kasa", password="KasaciOmenKral98!")

# The URL of your Instagram post
post_url = "https://www.instagram.com/reel/C-sPGLCtush/"

# Get the numeric media ID (primary key) from the post URL
media_pk = client.media_pk_from_url(post_url)

# Load previously processed comments from a file
try:
    with open("processed_comments.json", "r") as f:
        processed_comments = json.load(f)
except FileNotFoundError:
    processed_comments = {}

# Message content
message = (
    "VALODROP sayesinde Valorant kasaları açıp kazandıklarını gerçek VP'ye dönüştürebilirsin.\n"
    "✨Promo Kod✨: Cihan35\n"
    "Ayrıca aşağıdaki linkten kayıt olduğunda her satın alımında %10 fazladan VP kazanacaksın.\n"
    "Daha fazla kod ve soruların için Valodrop Discord sunucumuza davetlisin.\n\n"
    "Site Linki: valodrop.com/r/TRANQUILA\n"
    "Discord: https://discord.com/invite/cz2M68JXkC"
)

# Discord webhook URL
discord_webhook_url = "https://discord.com/api/webhooks/1273635393715306506/hGVcjG7DCEL9oIAMEza9GFstmHH86CAidVgj4Rvge4xpddfg90I2rsxbvv0vmEYXvOlA"

def send_to_discord(user_id, username):
    # Send the user ID and username to the Discord webhook
    data = {
        "content": f"DM sent to user ID: {user_id}, Username: @{username}"
    }
    response = requests.post(discord_webhook_url, json=data)
    if response.status_code == 204:
        print(f"User ID {user_id} (@{username}) successfully sent to Discord")
    else:
        print(f"Failed to send user ID and username to Discord. Status code: {response.status_code}")

while True:
    # Fetch all comments on the post using the media PK (primary key)
    comments = client.media_comments(media_pk)

    for comment in comments:
        comment_id = str(comment.pk)  # Convert comment ID to string for JSON compatibility
        user_id = comment.user.pk
        username = comment.user.username
        comment_text = comment.text.lower()

        # Log the comment being processed for debugging
        print(f"Processing comment ID: {comment_id} from user: @{username}")

        # Check if the comment contains the word "valorant" and hasn't been processed
        if "valorant" in comment_text:
            if comment_id not in processed_comments:
                try:
                    # Send DM to the user who commented
                    client.direct_send(message, [user_id])

                    # Mark the comment as processed
                    processed_comments[comment_id] = True

                    # Save the updated processed comments to a file
                    with open("processed_comments.json", "w") as f:
                        json.dump(processed_comments, f)

                    # Send the user ID and username to Discord
                    send_to_discord(user_id, username)

                    print(f"DM sent to user {user_id} (@{username}) for comment {comment_id}")

                except Exception as e:
                    print(f"Failed to send DM to user {user_id} (@{username}) for comment {comment_id}: {e}")
            else:
                print(f"Comment ID: {comment_id} has already been processed.")
        else:
            print(f"Comment ID: {comment_id} does not contain 'valorant', skipping.")

    # Sleep for a while before checking again
    time.sleep(30)  # Adjust the sleep time as needed

int(comment, comments_replied_to):
    if (
        TARGET_STRING in comment.body
        and comment.id not in comments_replied_to
        and comment.author != reddit_instance.user.me()
    ):
        # Log when the target string is found in a comment
        logger.info(f"String with '{TARGET_STRING}' found in comment {comment.id}")
        # Reply to the comment with the predefined message
        try:
            comment.reply(REPLY_MESSAGE)
            # Log that the bot has replied to the comment
            logger.info(f"Replied to comment {comment.id}")

            # Add the comment ID to the list of comments replied to
            comments_replied_to.append(comment.id)

            # Save the comment ID to the file
            with open("comments_replied_to.txt", "a") as f:
                f.write(comment.id + "\n")
        except prawcore.exceptions.Forbidden as forbidden_error:
            logger.warning(f"Permission error for comment {comment.id}: {forbidden_error}. Skipping.")
        except Exception as reply_error:
            logger.exception(f"Error while replying to comment {comment.id}: {reply_error}")

# Function to get saved comments
def get_saved_comments():
    if not os.path.isfile("comments_replied_to.txt"):
        # If the file doesn't exist, initialize an empty list
        comments_replied_to = []
    else:
        # Read the file and create a list of comments (excluding empty lines)
        with open("comments_replied_to.txt", "r") as f:
            comments_replied_to = [comment.strip() for comment in f.readlines() if comment.strip()]

    return comments_replied_to

# Main block to execute the bot
if __name__ == "__main__":
    # Log in to Reddit
    reddit_instance = bot_login()
    # Get the list of comments the bot has replied to from the file
    comments_replied_to = get_saved_comments()
    # Log the number of comments replied to
    logger.info(f"Number of comments replied to: {len(comments_replied_to)}")

    # Run the bot in an infinite loop
    while True:
        try:
            # Attempt to run the bot
            run_bot(reddit_instance, comments_replied_to)
        except Exception as e:
            # Log any general exceptions and sleep for the specified duration
            logger.exception(f"An error occurred: {e}")
            time.sleep(int(SLEEP_DURATION))  # Add a sleep after catching general exceptions
        except KeyboardInterrupt:
            logger.info("Bot terminated by user.")
            break

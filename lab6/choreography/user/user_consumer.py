import logging
import time
import schedule

from google.cloud import pubsub_v1


def create_subscription(project_id, topic_id, subscription_id):
    try:
        publisher = pubsub_v1.PublisherClient()
        subscriber = pubsub_v1.SubscriberClient()
        topic_path = publisher.topic_path(project_id, topic_id)
        subscription_path = subscriber.subscription_path(project_id, subscription_id)
        with subscriber:
            subscription = subscriber.create_subscription(
                request={"name": subscription_path, "topic": topic_path}
            )
        logging.info(f"Subscription created: {subscription}")
    except Exception as ex:
        logging.info(f"Error creating subscription {subscription_id} , the exception: {ex}.")
        logging.info(ex)


def pull_message(project, subscription):
    subscription_name = 'projects/{project_id}/subscriptions/{sub}'.format(
        project_id=project,
        sub=subscription
    )
    logging.info(f"Reading data from created: {subscription_name}")
    with pubsub_v1.SubscriberClient() as subscriber:
        future = subscriber.subscribe(subscription_name, callback)
        try:
            future.result()
        except Exception as ex:
            logging.info(ex)
            logging.info(f"Listening for messages on {subscription_name} threw an exception: {ex}.")
            time.sleep(30)


def callback(message):
    logging.info(f"Received {message}.")
    message.ack()


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    schedule.every().minute.at(':00').do(pull_message, "ada2025-450207", "order_status_user_sub")
    while True:
        schedule.run_pending()
        time.sleep(.1)

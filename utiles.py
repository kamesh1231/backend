import json
import os
from google.cloud import bigquery, pubsub_v1

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service-account.json"

def publish_msg(msg):

    TOPIC_NAME = "projects/on-the-money/topics/send_emails"
    publisher = pubsub_v1.PublisherClient()
    publish_future = publisher.publish(TOPIC_NAME, msg.encode())
    print(publish_future.result())

def less_selling_products():
    client = bigquery.Client()
    query = """
    SELECT product_name, COUNT(order_id) as total
    FROM `onthemoney.orders` o
    INNER JOIN `onthemoney.product` p 
    ON o.product_id = p.product_id
    GROUP BY product_name
    ORDER BY total 
    LIMIT 10
    """
    query_job = client.query(query)

    data = []
    for row in query_job:
        data.append({"product_name": row.product_name})

    return data

def high_purchasing_customers():
    client = bigquery.Client()
    query = """
    SELECT CONCAT(first_name,' ',last_name) as customer_name, COUNT(order_id) as total
    from `onthemoney.orders` o
    INNER JOIN `onthemoney.customer` c 
    ON o.customer_id = c.customer_id
    GROUP BY first_name, last_name
    ORDER BY total desc
    LIMIT 10
    """
    query_job = client.query(query)

    data = []
    for row in query_job:
        data.append({"customer_name": row.customer_name})

    return data

def recommend_low_selling_products_to_high_purchase_customers():
    customers = high_purchasing_customers()
    products = less_selling_products()
    template = open("less_selling-high_customers.html")
    data = {"customers": customers, "products": products, "template": template.read()}
    template.close()
    msg = json.dumps(data)
    return publish_msg(msg)


def high_selling_products():
    client = bigquery.Client()
    query = """
    SELECT product_name, COUNT(order_id) as total
    FROM `onthemoney.orders` o
    INNER JOIN `onthemoney.product` p 
    ON o.product_id = p.product_id
    GROUP BY product_name
    ORDER BY total desc
    LIMIT 10
    """
    query_job = client.query(query)

    data = []
    for row in query_job:
        data.append({"product_name": row.product_name})

    return data

def less_purchasing_customers():
    client = bigquery.Client()
    query = """
    SELECT CONCAT(first_name,' ',last_name) as customer_name, COUNT(order_id) as total
    from `onthemoney.orders` o
    INNER JOIN `onthemoney.customer` c 
    ON o.customer_id = c.customer_id
    GROUP BY first_name, last_name
    ORDER BY total 
    LIMIT 10
    """
    query_job = client.query(query)

    data = []
    for row in query_job:
        data.append({"customer_name": row.customer_name})

    return data

def recommend_high_selling_products_to_low_purchasing_customers():
    customers = less_purchasing_customers()
    products = high_selling_products()
    template = open("discounts.html")
    data = {"customers": customers, "products": products, "template": template.read()}
    template.close()
    msg = json.dumps(data)
    return publish_msg(msg)
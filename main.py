import os
from flask import Flask
from utiles import recommend_low_selling_products_to_high_purchase_customers, recommend_high_selling_products_to_low_purchasing_customers


PORT = os.environ.get("PORT",8080)

server = Flask(__name__)

@server.route("/home",methods=["GET"])
def home():
    recommend_low_selling_products_to_high_purchase_customers()
    recommend_high_selling_products_to_low_purchasing_customers()
    return {"message":"Message published to Pubsub"}, 200


if __name__ == "__main__":
    server.run("0.0.0.0",PORT)
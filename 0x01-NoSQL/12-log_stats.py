#!/usr/bin/env python3
""" script that provides some stats about Nginx logs stored in MongoDB """

from pymongo import MongoClient


def log_stats():
    """ provides some stats about Nginx logs """
    client = MongoClient('mongodb://127.0.0.1:27017')

    logs_collection = client.logs.nginx

    total = logs_collection.count_documents({})

    get = logs_collection.count_documents({"method": "GET"})

    post = logs_collection.count_documents({"method": "POST"})

    put = logs_collection.count_documents({"method": "PUT"})

    patch = logs_collection.count_documents({"method": "PATCH"})

    delete = logs_collection.count_documents({"method": "DELETE"})

    path = logs_collection.count_documents(
        {"method": "GET", "path": "/status"})

    print(f"{total} logs")

    for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        print(f"\tmethod {method}: {logs_collection.count_documents({'method': method})}")
    print(f"{path} status check")


if __name__ == "__main__":
    log_stats()

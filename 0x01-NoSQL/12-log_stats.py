#!/usr/bin/env python3
"""  provides some stats about Nginx logs stored in MongoDB """


from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    coll = client.logs.nginx

    accepted_method = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    # Aggregation pipeline
    pipeline = [
        # Stage 1: Match documents where 'methods' is in the specified list
        {
            "$match": {
                "method": {"$in": accepted_method}
            }
        },
        # Stage 2: Group by the 'methods' field and count number of documents
        {
            "$group": {
                "_id": "$method",  # Group by the 'methods' field
                "count": {"$sum": 1}  # Count number of documents in each group
            }
        }
    ]

    # Execute the aggregation
    result = coll.aggregate(pipeline)
    result_dict = {item['_id']: item['count'] for item in result}
    logs = coll.count_documents({})
    print("{} logs".format(logs))
    print("Methods:")
    for item in accepted_method:
        print("\tmethod {}: {}".format(item, result_dict.get(item, 0)))
    
    print(coll.count_documents({"$and": [
            {"method": {"$eq": "GET"}}, {"path": "/status"}
        ]}), "status check")

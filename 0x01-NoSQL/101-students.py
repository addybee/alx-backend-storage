#!/usr/bin/env python3
""" returns all students sorted by average score """


def top_students(mongo_collection):
    """ returns all students sorted by average score """
    pipeline = [
        {
            "$unwind": "$topics"  # Flatten the 'topic' array
        },
        {
            "$group": {
                "_id": "$_id",  # Group by the '_id' field value
                "name": {"$first": "$name"},  # Include the student's name
                # Calculate the average score within each group
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {
            # Sort by average score in descending order
            "$sort": {"averageScore": -1}
        }
    ]
    result =  list(mongo_collection.aggregate(pipeline))
    return result
    
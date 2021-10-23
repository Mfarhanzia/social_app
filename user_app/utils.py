import os
from django.db import connections, connection


def get_upload_path(instance, filename):
    """ creates unique-Path & filename for upload """
    ext = filename.split('.')[-1]
    filename = "%s%s.%s" % ('img', instance.pk, ext)

    return os.path.join(
        'profile_images', "user_id_{}".format(str(instance.id)),  filename
    )


def calculate_db_response_time():
    sqltime = 0.0 # Variable to store execution time
    for query in connection.queries:
        sqltime += float(query["time"])  # Add the time that the query took to the total
    query_total = 0
    for c in connections.all():
        query_total += len(c.queries)
    print("total queries:", query_total, "Page render: "+ str(sqltime)+ "sec for "+ str(len(connection.queries))+ " queries")

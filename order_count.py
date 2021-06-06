"""
sample code
"""
import sys
import json
from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark.streaming import StreamingContext


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: order-count.py <hostname> <port>", file=sys.stderr)
        sys.exit(-1)

    session = SparkSession.builder.master("local[2]")\
        .appName("PythonStreamingOrderCount")\
        .config("spark.ui.showConsoleProgress", "false")\
        .getOrCreate()

    sc = session.sparkContext
    sc.setLogLevel("ERROR")
    ssc = StreamingContext(sc, 5)

    orders = ssc.socketTextStream(sys.argv[1], int(sys.argv[2]))
    orders = orders.map(lambda rdd: json.loads(rdd))\
        .map(lambda r: (r['status'], 1))\
        .reduceByKey(lambda a, b: a+b)

    orders.pprint()

    ssc.start()
    ssc.awaitTermination()

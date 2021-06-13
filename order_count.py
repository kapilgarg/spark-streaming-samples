"""
sample code
"""
import sys
import json
from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from collections import defaultdict

CHECK_POINT_DIR = "c:\\temp\\"

def update(new_values, current_values):
    current_values = current_values or 0    
    return sum(new_values, current_values)




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
    ssc.checkpoint(CHECK_POINT_DIR)
    
    orders = ssc.socketTextStream(sys.argv[1], int(sys.argv[2]))
    
    #orders.pprint()

    orders = orders.map(lambda rdd: json.loads(rdd))\
        .map(lambda r: (r['status'], 1))\
        .reduceByKey(lambda a, b: a+b)
    
    # This will also create a cumulative state for the ordercount
    # add new number to the old orders count 
    total_count = orders.updateStateByKey(update)

    orders.pprint()
    total_count.pprint()

    ssc.start()
    ssc.awaitTermination()

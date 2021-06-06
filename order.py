import uuid
import random
import json

ORDER_STATUS = ['PLACED', 'INPROGRESS', 'COMPLETED', 'CANCELLED']


def generate_order():
    order = {
        'order_id': uuid.uuid4().hex,
        'status': ORDER_STATUS[random.randrange(0, len(ORDER_STATUS))]
    }
    return json.dumps(order)+'\n'

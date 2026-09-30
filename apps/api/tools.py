from data import customers, orders

def get_order(order_id):
    return orders.get(order_id)


def get_customer(customer_id):
    return customers.get(customer_id)

def get_refund_policy():
    with open("refund_policy.txt" ,"r") as file:
     return file.read()



def process_refund(order_id):
    order= orders.get(order_id)


    if order is None:

        return{


            "success":False,
            "reason":"order not found",
        }

    if order["refunded"]:
        return {

             "success":False,
             "reason":"This order has already been refunded",

        }


    validation = validate_refund(order_id)


    if not validation["eligible"]:
        return {

            "success":False,
            "reason":validation["reason"]
        }

    order["refunded"]=True

    return {



        "success":True,
        "order_id":order_id,
        "refund_amount":order["price"],
        "message":"Refunded processed successfully",
    }


def validate_refund(order_id):

    order = orders.get(order_id)

    if order is None:
        

        return {
            "eligible": False,
            "reason": "Order not found.",
        }

    if order["refunded"]:

          return {
            "eligible": False,
            "reason": "This Order has Already beed refunded.",
        }

    if order["status"]!="delivered":

          return {
            "eligible": False,
            "reason": "The Order has not been Recieved by the customer  yet.",
        }
    
    if order["days_since_delivery"] > 30:

          return {
            "eligible": False,
            "reason": "The Order is beyond refund period.",
        }
        

    return {
        "eligible": True,
        "reason": "Order is eligible for a refund.",
        "order_id": order_id,
        "refund_amount": order["price"],
    }



tools = [
    {
        "type": "function",
        "function": {
            "name": "get_customer",
            "description": "Get customer information using a customer ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "The unique ID of the customer.",
                    }
                },
                "required": ["customer_id"],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "get_order",
            "description": "Get order information using an order ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The unique ID of the order.",
                    }
                },
                "required": ["order_id"],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "validate_refund",
            "description": "Check whether an order is eligible for a refund according to the refund policy.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The unique ID of the order to validate for a refund.",
                    }
                },
                "required": ["order_id"],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "process_refund",
            "description": "Process a refund for an eligible order. The backend will verify refund eligibility before processing.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The unique ID of the order to refund.",
                    }
                },
                "required": ["order_id"],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "get_refund_policy",
            "description": "Get the e-commerce refund policy.",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    },
]
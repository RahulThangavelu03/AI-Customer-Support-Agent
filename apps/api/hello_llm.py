import os
import json

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)






customers = {
    "C001": {
        "id": "C001",
        "name": "Rahul",
        "email": "rahul@example.com",
    },
    "C002": {
        "id": "C002",
        "name": "Arun",
        "email": "arun@example.com",
    },
    "C003": {
        "id": "C003",
        "name": "Priya",
        "email": "priya@example.com",
    },
}








orders = {
    "O1001": {
        "id": "O1001",
        "customer_id": "C001",
        "product": "Wireless Headphones",
        "price": 4999,
        "status": "delivered",
        "days_since_delivery": 3,
        "refunded": False,
    },
    "O1002": {
        "id": "O1002",
        "customer_id": "C002",
        "product": "Mechanical Keyboard",
        "price": 3499,
        "status": "delivered",
        "days_since_delivery": 45,
        "refunded": False,
    },
    "O1003": {
        "id": "O1003",
        "customer_id": "C003",
        "product": "Smart Watch",
        "price": 7999,
        "status": "shipped",
        "days_since_delivery": None,
        "refunded": False,
    },
}

def get_order(order_id):
    return orders.get(order_id)


def get_customer(customer_id):
    return customers.get(customer_id)


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

    }
]


def run_agent(user_question):

 
    messages=[{
    "role": "system",
    "content": """
You are an e-commerce customer support agent.

Rules:
- Use tools whenever customer, order, or refund information is needed.
- Never invent or assume facts.
- Never create or change refund policy rules.
- Refund eligibility must come from validate_refund.
- Only state facts provided by the tools.
- Do not speculate about why an order has a particular status.
- Do not give unsolicited advice.
- Keep every response to 1-2 short sentences.
"""
},]


    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=tools,
    )

    message = response.choices[0].message

    if message.tool_calls:

        messages.append(message)

        for tool_call in message.tool_calls:

            
            
            arguments = json.loads(tool_call.function.arguments)

            if tool_call.function.name == "get_customer":
              result = get_customer(arguments["customer_id"])  

            elif tool_call.function.name == "get_order":
               result = get_order(arguments["order_id"])

            elif tool_call.function.name=="validate_refund":
                result=validate_refund(arguments["order_id"])



            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result),
                }
            )

        final_response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=tools,
        )

        return final_response.choices[0].message.content

    return message.content


question = input("You: ")

answer = run_agent(question)

print("Agent:", answer)


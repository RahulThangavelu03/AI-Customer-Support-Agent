import os
import json

from dotenv import load_dotenv
from openai import OpenAI

from tools import (
    tools,
    get_customer,
    get_order,
    validate_refund,
    process_refund,
    get_refund_policy,
)

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)


def run_agent(user_question):

    activity_logs = []

    messages = [
        {
            "role": "system",
            "content": """
You are an e-commerce customer support agent.

Rules:
- Use tools whenever customer, order, or refund information is needed.
- Never invent or assume facts.
- Never create or change refund policy rules.
- Refund eligibility must come from validate_refund.
- If the customer explicitly asks to process a refund, validate the order first.
- Only process a refund if validate_refund says the order is eligible.
- Only state facts provided by the tools.
- Do not speculate.
- Do not give unsolicited advice.
- Keep every response to 1-2 short sentences.
""",
        },
        {
            "role": "user",
            "content": user_question,
        }
    ]

    while True:

        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=tools,
        )

        message = response.choices[0].message

        

        if not message.tool_calls:
           return {
                "response": message.content,
                 "activity_logs": activity_logs,
    }

        messages.append(message)

       
        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            # Log the tool request
            activity_logs.append({
                "type": "tool_requested",
                "tool": tool_name,
                "arguments": arguments,
            })

            # Execute the requested tool
            if tool_name == "get_customer":
                result = get_customer(arguments["customer_id"])

            elif tool_name == "get_order":
                result = get_order(arguments["order_id"])

            elif tool_name == "validate_refund":
                result = validate_refund(arguments["order_id"])

            elif tool_name == "process_refund":
                result = process_refund(arguments["order_id"])

            elif tool_name == "get_refund_policy":
                result = get_refund_policy()

            else:
                result = {
                    "error": f"Unknown tool: {tool_name}"
                }

            # Log the actual tool result
            activity_logs.append({
                "type": "tool_result",
                "tool": tool_name,
                "result": result,
            })

            # Send the result back to the LLM
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result),
            })
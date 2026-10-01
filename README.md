# AI Customer Support Agent

An AI-powered e-commerce customer support agent built with **Next.js, FastAPI, Python, and an LLM**. The agent answers customer questions using mock CRM data and processes refund requests through tool calling, with refund eligibility enforced by backend business rules.

## Features

- **AI-powered customer support:** Answers customer questions using customer, order, and refund-policy information.
- **LLM tool calling:** Uses function calling to retrieve customer details, look up orders, check the refund policy, validate refunds, and process eligible refunds.
- **Refund policy enforcement:** Validates order status, delivery date, refund eligibility, and previous refund status before processing.
- **Mock CRM:** Includes 15 mock customers and 15 orders for testing different scenarios.
- **Admin activity dashboard:** Displays the agent's tool requests, arguments, and results.
- **Backend API:** A FastAPI endpoint connects the customer chat interface to the agent.
- **Free-model support:** Uses OpenRouter's model API, configured through an environment variable.

## Tech Stack

**Frontend**

- Next.js
- React
- TypeScript
- Tailwind CSS

**Backend**

- Python
- FastAPI
- OpenAI Python SDK
- OpenRouter API

## Architecture

```text
Customer
   |
   v
Next.js Chat Interface
   |
   | POST /chat
   v
FastAPI Backend
   |
   v
LLM Agent (OpenRouter)
   |
   | Tool calls
   v
Python Tool Functions
   |
   +-- Get customer
   +-- Get order
   +-- Get refund policy
   +-- Validate refund
   +-- Process refund
   |
   v
Mock CRM Data
   |
   v
Tool results returned to the LLM
   |
   v
Final response to the customer
```

The LLM decides which tools to request based on the customer's message. Python executes those tools and returns their results to the LLM. The agent continues until the model produces a final response.

Refund eligibility is determined by backend validation rather than trusting the model's decision.

## Refund Policy

The agent follows these rules:

1. Only delivered orders are eligible for refunds.
2. Refund requests must be made within 30 days of delivery.
3. An order that has already been refunded cannot be refunded again.
4. The refund amount equals the original order price.
5. Refund eligibility must be validated before processing.
6. The backend rechecks eligibility when processing a refund.

## Project Structure

```text
AI-Customer-Support-Agent/
├── apps/
│   ├── api/
│   │   ├── main.py
│   │   ├── agent.py
│   │   ├── tools.py
│   │   ├── data.py
│   │   ├── refund_policy.txt
│   │   └── requirements.txt
│   └── web/
│       ├── app/
│       │   ├── page.tsx
│       │   └── admin/
│       │       └── page.tsx
│       ├── package.json
│       └── ...
└── README.md
```

## Prerequisites

- Python 3.11 or later
- Node.js and npm
- An OpenRouter API key

The project uses mock in-memory data, so a separate database is not required.

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/RahulThangavelu03/AI-Customer-Support-Agent.git
cd AI-Customer-Support-Agent
```

### 2. Configure the backend

Open a terminal and navigate to the API directory:

```bash
cd apps/api
```

Create and activate a virtual environment.

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the Python dependencies:

```bash


pip install -r requirements.txt
```

Create a `.env` file inside `apps/api/`:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
```

Replace the placeholder with your own API key. Do not commit this file.

Start the backend:

```bash
uvicorn main:app --reload
```

The API will be available at:

`http://localhost:8000`

API documentation:

`http://localhost:8000/docs`

Health check:

`http://localhost:8000/health`

### 3. Configure the frontend

Open a second terminal and navigate to the web directory:

```bash
cd apps/web
npm install
```

Start the Next.js development server:

```bash
npm run dev
```

Open the application at:

`http://localhost:3000`

### 4. Use the application

- Open the customer support page and ask a question about an order.
- Try a refund request using one of the mock order IDs.
- Open `/admin` to inspect the tool requests and results recorded for the current browser session.

## Example Scenarios

The mock data includes orders with different statuses and delivery dates.

| Scenario              | Example order | Expected behavior                                        |
| --------------------- | ------------- | -------------------------------------------------------- |
| Eligible refund       | `O1004`       | Eligible if not already refunded                         |
| Outside refund period | `O1002`       | Refund denied because delivery was more than 30 days ago |
| Already refunded      | `O1011`       | Refund denied                                            |
| Not yet delivered     | `O1003`       | Refund denied                                            |

Refund outcomes depend on the current state of the in-memory mock data. A successful refund changes that order's state while the backend process is running.

## API Endpoint

### `POST /chat`

Accepts a customer message and returns the agent's response and activity logs.

Example request:

```json
{
  "message": "Can I get a refund for order O1004?"
}
```

The response contains:

- `response`: the agent's reply.
- `activity_logs`: tool requests and tool results generated during that interaction.

## Design Decisions

- **Backend-authoritative validation:** The LLM cannot override refund eligibility rules.
- **Tool-based interaction:** The agent retrieves information through explicit Python functions rather than inventing CRM data.
- **Separation of concerns:** The Next.js frontend handles the interface, FastAPI exposes the API, and Python functions implement the business rules.
- **Mock data:** Keeps the assignment self-contained without requiring a database or external CRM.

## Current Limitations

- Customer and order data are mock data stored in memory.
- Refund state is not persisted to a database and resets when the backend process restarts.
- Admin activity logs are stored in browser `sessionStorage`. They are session-based, not a persistent or real-time audit log.
- The application is a take-home assignment prototype and is not intended for production use without additional authentication, authorization, persistence, and security controls.

## Future Improvements

- Persistent storage for customers, orders, and refund history.
- Authentication and role-based access for customers and administrators.
- Persistent audit logs and real-time activity updates.
- Automated tests for refund-policy rules and API endpoints.
- Improved error handling, observability, and deployment configuration.

## Author

**Rahul Thangavelu**

GitHub: [RahulThangavelu03](https://github.com/RahulThangavelu03)

---

This project was built as a practical exploration of LLM tool calling, backend business-rule enforcement, and full-stack AI application development.

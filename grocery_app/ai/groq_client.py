from groq import Groq
from django.conf import settings

# Create Groq client
client = Groq(api_key=settings.GROQ_API_KEY)


def understand_user_query(user_message):
    """
    Converts the user's question into structured JSON.
    Groq should NOT answer the question.
    It should only identify the intent.
    """

    prompt = f"""
You are an NLP engine for a Grocery Store.

Your job is NOT to answer questions.

Your job is ONLY to convert the user's message into JSON.

Supported intents:

1. search_product
2. search_category
3. product_price
4. product_stock
5. available_products
6. out_of_stock
7. cheapest_product
8. expensive_product
9. total_products
10. total_categories
11. total_orders
12. pending_orders

Return ONLY JSON.

User:
{user_message}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """
                You are an API.
                 Return ONLY valid JSON.
                 Do NOT use markdown.
                Do NOT use ```.
                Do NOT explain.
                Return exactly one JSON object.
               """
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content
import json

from grocery_app.models import Product, Category, Order
from grocery_app.ai.groq_client import understand_user_query


def get_chatbot_response(user_message):
    """
    Main chatbot function.
    """

    try:
        groq_response = understand_user_query(user_message)
        
        print("=" * 50)
        print("RAW GROQ RESPONSE")
        print(groq_response)
        print("=" * 50)

        print("Groq JSON:", groq_response)
        
        groq_response = groq_response.replace("```json", "")
        groq_response = groq_response.replace("```", "")
        groq_response = groq_response.strip()

        print("=" * 50)
        print("CLEAN JSON")
        print(groq_response)
        print("=" * 50)

        data = json.loads(groq_response)

    except Exception as e:
        return f"Error understanding your request.\n{e}"

    intent = data.get("intent")

    # -----------------------------
    # Search Product
    # -----------------------------
    if intent == "search_product":

        product = data.get("product", "")

        products = Product.objects.filter(name__icontains=product)

        if not products.exists():
            return f"Sorry, I couldn't find '{product}'."

        answer = ""

        for p in products:

            answer += (
                f"Product : {p.name}\n"
                f"Category : {p.category.name}\n"
                f"Price : ₹{p.price}\n"
                f"Stock : {p.stock}\n\n"
            )

        return answer

    # -----------------------------
    # Search Category
    # -----------------------------
    elif intent == "search_category":

        category = data.get("category", "")

        products = Product.objects.filter(
            category__name__icontains=category
        )

        if not products.exists():
            return "No products found."

        answer = f"{category} Products\n\n"

        for p in products:

            answer += f"{p.name} - ₹{p.price}\n"

        return answer

    # -----------------------------
    # Total Products
    # -----------------------------
    elif intent == "total_products":

        total = Product.objects.count()

        return f"There are {total} products."

    # -----------------------------
    # Total Categories
    # -----------------------------
    elif intent == "total_categories":

        total = Category.objects.count()

        return f"There are {total} categories."

    # -----------------------------
    # Pending Orders
    # -----------------------------
    elif intent == "pending_orders":

        total = Order.objects.filter(status="pending").count()

        return f"There are {total} pending orders."

    # -----------------------------
    # Total Orders
    # -----------------------------
    elif intent == "total_orders":

        total = Order.objects.count()

        return f"There are {total} orders."

    # -----------------------------
    # Unknown Intent
    # -----------------------------
    return "Sorry, I couldn't understand your request."
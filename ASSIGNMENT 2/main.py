from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()

# ── Temporary data — acting as our database for now ──────────
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics", "in_stock": False},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": True}
]

@app.get("/")
def home():
    return {"message": "FastAPI Assignment"}

# ── Endpoint 0 — Home ────────────────────────────────────────
@app.get('/')
def home():
    return {'message': 'Welcome to our E-commerce API'}

                                                                                 # ASSIGNMENT 1
# ── Endpoint 1 — Return all products ──────────────────────────
@app.get('/products')                                                            #Q.1
def get_all_products():
    return {'products': products, 'total': len(products)}

# ── Endpoint 2 — Return specific product by its category ──────────────────
@app.get('/products/category/{category_name}')                                   #Q.2
def get_product_by_category(category_name : str):
    result = [p for p in products if p["category"] == category_name] 
    if not result: 
        return {"error": "No products found in this category"} 
    return {"category": category_name, "products": result, "total": len(result)}

#── Endpoint 3 — Return product by its availability ──────────────────
@app.get('/products/in_stock')                                                   #Q.3
def get_instock_product(in_stock: bool = True):
    result = [p for p in products if p['in_stock'] == in_stock]
    if not result:
        return {'error': 'Product not found'}
    return {'in_stock_products': result, 'count': len(result)}

#── Endpoint 4 — Return products summary ──────────────────
@app.get('/products/store/summary')                                              #Q.4
def get_store_summary():
    instock_count = len([p for p in products if p["in_stock"]])
    out_of_stock_count = len(products) - instock_count
    categories = list(set([p["category"] for p in products]))
    return {
        "store_name": "My E-commerce Store",
        "total_products": len(products),
        "in_stock": instock_count,
        "out_of_stock": out_of_stock_count,
        "categories": categories,
    }

# ── Endpoint 5 — Search Products by Name  ──────────────────
@app.get('/products/search/{keyword}')                                           #Q.5
def get_instock_product(keyword : str ):
    key = keyword.strip().lower()
    matched = [p for p in products if key in p['name'].lower()]

    if not matched:
        return {"message": "No products matched", "products": [], "count": 0}

    return {"products": matched, "count": len(matched)}

# ── Endpoint 6 — Search deals  ──────────────────
@app.get('/products/deals')                                                      #BONUS
def get_deals():
    if not products:
        return {"error": "No products available"}
    cheapest = min(products, key=lambda p: p["price"])
    expensive = max(products, key=lambda p: p["price"])
    return {
        "best_deal": cheapest,
        "premium_pick": expensive,
    }

                                                                    # assignment 2
# ── Endpoint 7 — filter the product  ──────────────────                                                                   
@app.get("/products/filter")                                        #Q1
def filter_products(
        category: Optional[str] = None,
        max_price: Optional[int] = None,
        min_price: Optional[int] = None):

    result = products

    if category:
        result = [p for p in result if p["category"].lower() == category.lower()]

    if max_price is not None:
        result = [p for p in result if p["price"] <= max_price]

    if min_price is not None:
        result = [p for p in result if p["price"] >= min_price]

    return result

# ── Endpoint 7 — Search product by product ID  ──────────────────
@app.get("/products/{product_id}/price")                            #Q.2
def get_product_price(product_id: int):

    for product in products:
        if product["id"] == product_id:
            return {
                "name": product["name"],
                "price": product["price"]
            }

    return {"error": "Product not found"}

# ── Endpoint 9 — post valid feedback  ──────────────────
orders = []
feedback = []

class customer_feedback(BaseModel):                                  #Q.3
    customer_name : str = Field(..., min_length=2)
    product_id : int = Field(..., gt=0)
    rating : int = Field(..., ge=1, le=5)
    comment: Optional[str] = Field(None, max_length=300)

@app.post("/feedback")
def submit_feedback(data : customer_feedback):
    feedback.append(data.dict())
    return {
        "message":        "Feedback submitted successfully",
        "feedback":       data.dict(),
        "total_feedback": len(feedback),
    }

# ── Endpoint 10 — show summary  ──────────────────
@app.get('/products/summary')                                       # Q.4
def get_store_summary():
    total_products = len(products)
    instock_count = len([p for p in products if p["in_stock"]])
    out_of_stock_count = total_products - instock_count
    cheapest = min(products, key=lambda p: p["price"])
    expensive = max(products, key=lambda p: p["price"])
    categories = sorted(list(set([p["category"] for p in products])))

    return {
        "total_products": total_products,
        "in_stock_count": instock_count,
        "out_of_stock_count": out_of_stock_count,
        "most_expensive": {"name": expensive["name"], "price": expensive["price"]},
        "cheapest": {"name": cheapest["name"], "price": cheapest["price"]},
        "categories": categories
    }

# ── Endpoint 11 — post bulk order  ──────────────────
class order_item(BaseModel):                                        # Q. 5
    product_id : int = Field(...,gt = 0)
    quantity : int = Field(..., ge = 1, le= 50)

class bulk_order(BaseModel):
    company_name : str = Field(..., min_length=2) 
    company_email : str = Field(..., min_length=5)
    items : List[order_item] = Field(...,min_items=1)

@app.post('/orders/bulk')
def OrderBulk(order : bulk_order):
    confirmed, failed, grand_total = [], [], 0
    for item in order.items:
        product = next((p for p in products if p["id"] == item.product_id), None)
        if not product:
            failed.append({"product_id": item.product_id, "reason": "Product not found"})
        elif not product["in_stock"]:
            failed.append({"product_id": item.product_id, "reason": f"{product['name']} is out of stock"})
        else:
            subtotal = product["price"] * item.quantity
            grand_total += subtotal
            confirmed.append({"product": product["name"], "qty": item.quantity, "subtotal": subtotal})
    return {"company": order.company_name,
            "confirmed": confirmed,
            "failed": failed,
             "grand_total": grand_total}

# ── Endpoint 12 — order status tracker  ──────────────────
class Order(BaseModel):                                             #bonus
    product_id: int
    quantity: int


@app.post("/orders")
def create_order(order: Order):

    order_data = {
        "id": len(orders) + 1,
        "product_id": order.product_id,
        "quantity": order.quantity,
        "status": "pending"
    }

    orders.append(order_data)

    return order_data


@app.get("/orders/{order_id}")
def get_order(order_id: int):

    for order in orders:
        if order["id"] == order_id:
            return order

    return {"error": "Order not found"}


@app.patch("/orders/{order_id}/confirm")
def confirm_order(order_id: int):

    for order in orders:
        if order["id"] == order_id:
            order["status"] = "confirmed"
            return order

    return {"error": "Order not found"}


    

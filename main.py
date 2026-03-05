from fastapi import FastAPI, Query
 
app = FastAPI()
 
# ── Temporary data — acting as our database for now ──────────
products = [
    {'id': 1, 'name': 'Wireless Mouse', 'price': 499,  'category': 'Electronics', 'in_stock': True },
    {'id': 2, 'name': 'Notebook',       'price':  99,  'category': 'Stationery',  'in_stock': True },
    {'id': 3, 'name': 'USB Hub',        'price': 799, 'category': 'Electronics', 'in_stock': False},
    {'id': 4, 'name': 'Pen Set',        'price':  49, 'category': 'Stationery',  'in_stock': True },
    {'id': 5, 'name': 'Laptop Stand',       'price': 449, 'category': 'Stationery',  'in_stock': True },
    {'id': 6, 'name': 'Mechanical Keyboard','price': 999, 'category': 'Electronics', 'in_stock': True },
    {'id': 7, 'name': 'Webcam',             'price': 1999, 'category': 'Electronics',  'in_stock': False},
]
 
# ── Endpoint 0 — Home ────────────────────────────────────────
@app.get('/')
def home():
    return {'message': 'Welcome to our E-commerce API'}
 
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
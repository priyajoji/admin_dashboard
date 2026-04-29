from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="shopuser",
    password="password123",
    database="ecommerce_db_2"
)

cursor = db.cursor(dictionary=True)

# ---------------- PRODUCT INVENTORY ----------------

@app.route("/products", methods=["GET"])
def get_products():
    cursor.execute("""
        SELECT p.*, c.category_name, s.supplier_name
        FROM Product_Details p
        LEFT JOIN Product_Category c ON p.category_id = c.category_id
        LEFT JOIN Supplier s ON p.supplier_id = s.supplier_id
    """)
    return jsonify(cursor.fetchall())


@app.route("/products", methods=["POST"])
def add_product():
    data = request.json
    cursor.execute("""
        INSERT INTO Product_Details (product_name, product_price, product_status, category_id, supplier_id)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        data["product_name"],
        data["product_price"],
        data["product_status"],
        data["category_id"],
        data["supplier_id"]
    ))
    db.commit()
    return jsonify({"message": "Product added"})

@app.route("/products/<int:id>", methods=["PUT"])
def update_product(id):
    data = request.json

    cursor.execute("""
        UPDATE Product_Details
        SET product_name=%s,
            product_price=%s,
            product_status=%s,
            category_id=%s,
            supplier_id=%s
        WHERE product_id=%s
    """, (
        data["product_name"],
        data["product_price"],
        data["product_status"],
        data["category_id"],
        data["supplier_id"],
        id
    ))

    db.commit()
    return jsonify({"message": "Product updated"})


@app.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    cursor.execute("DELETE FROM Product_Details WHERE product_id=%s", (id,))
    db.commit()
    return jsonify({"message": "Product deleted"})


# ---------------- CUSTOMERS ----------------

@app.route("/customers", methods=["GET"])
def get_customers():
    cursor.execute("SELECT * FROM Customer")
    return jsonify(cursor.fetchall())


# ---------------- SALES ----------------

@app.route("/sales", methods=["GET"])
def get_sales():
    cursor.execute("""
        SELECT o.order_no, o.order_date, o.order_amount, c.customer_name
        FROM Orders o
        JOIN Customer c ON o.customer_id = c.customer_id
        ORDER BY o.order_date DESC
    """)
    return jsonify(cursor.fetchall())


if __name__ == "__main__":
    app.run(debug=True)
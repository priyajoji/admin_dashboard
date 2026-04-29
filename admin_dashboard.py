import streamlit as st
import requests
import pandas as pd

API = "http://127.0.0.1:5000"

st.set_page_config(
    page_title="Admin Dashboard",
    layout="wide",
    page_icon="🛒"
)

# ---------------- THEME UI ----------------
st.markdown("""
    <style>
/* ================= GLOBAL ================= */
.main {
    background-color: #0b1220;
    color: #e5e7eb;
}

/* page padding */
.block-container {
    padding-top: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

/* headings */
h1, h2, h3 {
    color: #f9fafb;
    font-weight: 600;
}

/* normal text */
p, span, label, li {
    color: #cbd5e1 !important;
}

/* ================= SIDEBAR (NAV BAR AREA) ================= */
section[data-testid="stSidebar"] {
    background-color: #0f172a;
    border-right: 1px solid #1e293b;
}

/* sidebar text */
section[data-testid="stSidebar"] * {
    color: #cbd5e1 !important;
}

/* sidebar header */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2 {
    color: #f8fafc !important;
}

/* sidebar radio/selectbox active item */
section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background-color: #1e293b;
    border-radius: 8px;
}

/* selected item highlight */
section[data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] {
    background-color: #2563eb;
    color: white !important;
    border-radius: 8px;
}

/* ================= METRICS ================= */
div[data-testid="metric-container"] {
    background-color: #111c33;
    border-radius: 12px;
    padding: 16px;
    border: 1px solid #1e293b;
}

div[data-testid="metric-container"] * {
    color: #f1f5f9 !important;
}

/* ================= TABLES ================= */
.stDataFrame {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #1e293b;
}

/* ================= INPUT FIELDS ================= */
input, textarea, select {
    background-color: #111c33 !important;
    color: #e5e7eb !important;
    border: 1px solid #1e293b !important;
    border-radius: 8px !important;
}

/* focus effect */
input:focus, textarea:focus {
    border-color: #3b82f6 !important;
    outline: none !important;
}

/* ================= BUTTONS ================= */
.stButton > button {
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
    border: none;
    padding: 0.5rem 1rem;
    transition: 0.2s ease;
}

.stButton > button:hover {
    background-color: #1d4ed8;
}

/* danger buttons (delete etc.) */
.stButton > button[kind="primary"] {
    background-color: #ef4444;
}
</style>
""", unsafe_allow_html=True)

st.title("🛒 E-Commerce Admin Dashboard")

menu = st.sidebar.selectbox(
    "Navigation",
    ["Inventory", "Customers", "Sales"]
)

# ---------------- INVENTORY PAGE ----------------
if menu == "Inventory":
    st.header("📦 Product Inventory")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("➕ Add Product")

        with st.container():
            name = st.text_input("Product Name")
            price = st.number_input("Price", min_value=0.0)
            status = st.selectbox("Status", ["Available", "Out of Stock"])
            category = st.number_input("Category ID", min_value=1)
            supplier = st.number_input("Supplier ID", min_value=1)

            if st.button("Add Product", use_container_width=True):
                payload = {
                    "product_name": name,
                    "product_price": price,
                    "product_status": status,
                    "category_id": category,
                    "supplier_id": supplier
                }
                requests.post(f"{API}/products", json=payload)
                st.success("Product added successfully")

    with col2:
        st.subheader("📋 Product List")

        res = requests.get(f"{API}/products").json()
        df = pd.DataFrame(res)

        st.dataframe(df, use_container_width=True)

        st.divider()

        delete_id = st.number_input("Delete Product ID", min_value=1)

        if st.button("Delete Product", type="primary"):
            requests.delete(f"{API}/products/{delete_id}")
            st.warning("Product deleted")

        st.divider()
        st.subheader("✏️ Update Product")

        update_id = st.number_input("Product ID to Update", min_value=1, step=1)

        u_name = st.text_input("New Product Name")
        u_price = st.number_input("New Price", min_value=0.0)
        u_status = st.selectbox("New Status", ["Available", "Out of Stock"])
        u_category = st.number_input("New Category ID", min_value=1)
        u_supplier = st.number_input("New Supplier ID", min_value=1)

        if st.button("Update Product"):
            payload = {
            "product_name": u_name,
            "product_price": u_price,
            "product_status": u_status,
            "category_id": u_category,
            "supplier_id": u_supplier
       }
            requests.put(f"{API}/products/{update_id}", json=payload)
            st.success("Product updated successfully")

# ---------------- CUSTOMERS PAGE ----------------
elif menu == "Customers":
    st.header("👥 Customers Overview")

    res = requests.get(f"{API}/customers").json()
    df = pd.DataFrame(res)

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Customers", len(df))

    with col2:
        st.metric("Active Records", len(df))

    st.dataframe(df, use_container_width=True)


# ---------------- SALES PAGE ----------------
elif menu == "Sales":
    st.header("📊 Sales Dashboard")

    res = requests.get(f"{API}/sales").json()
    df = pd.DataFrame(res)

    if not df.empty:
        df["order_amount"] = pd.to_numeric(df["order_amount"], errors="coerce")
        total_sales = df["order_amount"].sum()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("💰 Total Sales", f"₹ {total_sales:,.2f}")

        with col2:
            st.metric("📦 Orders", len(df))

        with col3:
            st.metric("📅 Avg Order", f"₹ {df['order_amount'].mean():.2f}")

        st.divider()

        st.subheader("Sales Table")
        st.dataframe(df, use_container_width=True)

        st.subheader("Sales Trend")
        st.line_chart(df.groupby("order_date")["order_amount"].sum())
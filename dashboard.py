
from itertools import product
import pandas as pd
import psycopg2
import streamlit as st
import plotly.express as px
from pass_file import *

st.title('Summary Dashboard')

def get_data(cursor, query):
    cursor.execute(query)
    data = cursor.fetchall()
    df = pd.DataFrame(data)
    return df

import time
start_time = time.time()

#establishing the connection
conn = psycopg2.connect(
    database="DBMS",
    user='postgres',
    password=password_current,
    host='127.0.0.1',
    port= '5432')

#Creating a cursor object using the cursor() method
cursor = conn.cursor()


days = st.selectbox('Choose previous "n" days', ( 30, 180, 365))

top_n = st.selectbox('Choose top "n" records', ( 3, 5, 10, 20))

top_5_customers = '''SELECT orders.customer_id, sum(order_items.quantity * products.price) as total_value
FROM orders 
INNER JOIN order_items
      ON orders.order_id=order_items.order_id
INNER JOIN products
      ON order_items.product_id=products.product_id

WHERE orders.purchase_time > current_date - {}
GROUP BY orders.customer_id

ORDER BY total_value DESC LIMIT {}'''.format(days, int(top_n))

top_5_product_categories = '''SELECT products.product_category, sum(order_items.quantity * products.price) as total_value
FROM order_items 
INNER JOIN products
      ON order_items.product_id=products.product_id
INNER JOIN orders
      ON orders.order_id=order_items.order_id
WHERE orders.purchase_time > current_date - {}
GROUP BY products.product_category
ORDER BY total_value DESC LIMIT {}'''.format(days, int(top_n))

customers = get_data(cursor, top_5_customers)
customers.columns = ['Top Customer IDs', 'Total Purchase $']
# customers['Total Purchase $'] = customers['Total Purchase $'].round(2)
customers.index = range(1,min(top_n, len(customers))+1)
st.write(customers)

product_cats = get_data(cursor, top_5_product_categories)
product_cats.columns = ['Top Product Categories', 'Total Purchase $']
# product_cats['Total Purchase $'] = product_cats['Total Purchase $'].round(2)
product_cats.index = range(1,min(top_n, len(product_cats))+1)
st.write(product_cats)

fig = px.bar(product_cats, x='Top Product Categories', y='Total Purchase $')
st.plotly_chart(fig)

st.header("Monthly Revenue")
query = '''SELECT orders.purchase_time, sum(order_items.quantity * products.price) as revenue
FROM orders 
INNER JOIN order_items
      ON orders.order_id=order_items.order_id
INNER JOIN products
      ON order_items.product_id=products.product_id
GROUP BY orders.purchase_time'''

cursor.execute(query)
data = cursor.fetchall()
runtime = time.time() - start_time

df = pd.DataFrame(data)

df.columns = ['Date', 'Revenue']


df['Date'] = pd.to_datetime(df['Date'])
df2 = df.set_index("Date").groupby([pd.Grouper(freq='M')])["Revenue"].sum()
fig = px.line(df2)
st.plotly_chart(fig)

st.write("(results in %s seconds)" % (round(runtime, 3)))
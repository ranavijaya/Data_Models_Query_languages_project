import time
start_time = time.time()
from pass_file import *

import pandas as pd
import psycopg2
from datetime import datetime as dt
import streamlit as st

def get_sublevels(outer_level,option, sublevel, table_name):    
    query = """SELECT DISTINCT {} from {}
               where {} = '{}'""".format(sublevel, table_name, outer_level, option)
    cursor.execute(query)
    sublevels = cursor.fetchall()
    sublevels = tuple([i[0] for i in sublevels])
    return sublevels

#establishing the connection
conn = psycopg2.connect(
    database="DBMS",
    user='postgres',
    password=password_current,
    host='127.0.0.1',
    port= '5432')

#Creating a cursor object using the cursor() method
cursor = conn.cursor()
cursor.execute("""SELECT distinct product_category from products""")
data = cursor.fetchall()
all_product_categories = [i[0] for i in data]

cursor.execute("""SELECT customer_id, customer_city from customers""")
data = cursor.fetchall()
cust_ids = [i[0] for i in data]
cust_cities = [i[1] for i in data]

st.title("Customer Place Order")
customer_id = st.number_input('Enter Custumer ID', min_value=min(cust_ids), max_value=max(cust_ids), value=min(cust_ids), step=1)
cust_city = [cust_cities[i] for i in range(len(cust_ids)) if cust_ids[i] == customer_id ][0]

prod_cat_options = st.selectbox('Choose Product Category', tuple(all_product_categories))

cursor.execute("""SELECT DISTINCT product_id, product_name, price, seller_id from products
                  where product_category = '{}'""".format(prod_cat_options))
data = cursor.fetchall()
prod_ids = [i[0] for i in data]
prod_names = [i[1] for i in data]
prod_prices = [i[2] for i in data]
seller_ids =  [i[3] for i in data]

prod_opt = st.selectbox('Choose Product Name', prod_names)
prod_id = [prod_ids[i] for i in range(len(prod_ids)) if prod_names[i] == prod_opt ][0]
price = [prod_prices[i] for i in range(len(prod_prices)) if prod_names[i] == prod_opt ][0]
seller_id = [seller_ids[i] for i in range(len(seller_ids)) if prod_names[i] == prod_opt ][0]


del_time_query = """SELECT time_to_deliver, seller_city FROM distances
WHERE seller_id = {} AND customer_city = '{}'""".format(str(seller_id), cust_city)

cursor.execute(del_time_query)
data = cursor.fetchall()
time_to_del = [i[0] for i in data][0]
seller_city = [i[1] for i in data][0]


Quantity = st.slider('Quantity', min_value=1, max_value=10, value=1, step=1)
payment_type = st.selectbox('Payment Method', ( "debit_card", "credit_card", "food_stamp", "cash" , "gift_card"))

st.write('$' + str(round(price*Quantity, 2)))
st.write("Delivery time: {} hours.".format(time_to_del))

order_id = int(str(dt.now().year)[-2:] + ('0' + str(dt.now().day))[-2:] + ('0' + str(dt.now().month))[-2:] + ('000' + str(customer_id))[-2:])

vals_1 = ', '.join([str(order_id), str(customer_id), 'CURRENT_DATE', "'{}'".format(payment_type)])
vals_2 = ', '.join([str(order_id), str(prod_id), str(Quantity)])

insert_query1 = """INSERT into orders (order_id, customer_id, purchase_time, payment_type) VALUES (""" + vals_1 + ") ON CONFLICT DO NOTHING"
insert_query2 = """INSERT into order_items (order_id ,product_id, quantity) VALUES (""" + vals_2 + ")"

# st.write("--- Runtime %s seconds ---" % (round(time.time() - start_time, 3)))

start_button = st.empty()
if start_button.button('Order',key='start'):
    start_button.empty()
    cursor.execute(insert_query1)
    cursor.execute(insert_query2)
    st.write("Item added to order {}   x   {}".format(prod_opt, Quantity))
    st.write('Select more items from above menu.')
    st.write("(results in %s seconds)" % (round(time.time() - start_time, 3)))

    conn.commit()
    conn.close()
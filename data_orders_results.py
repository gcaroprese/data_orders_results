# -*- coding: utf-8 -*-
"""AnyoneAI1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1N0NRrtK8s7QDJEGFIrdqr3JzD7Yl91Xx
"""

import requests
from collections import defaultdict

def import_data_files():
  r = requests.get('https://raw.githubusercontent.com/anyoneai/notebooks/main/customers_and_orders/data/customers.csv')
  with open('./sample_data/customers.csv', 'wb') as f:
    f.write(r.content)

  r = requests.get('https://raw.githubusercontent.com/anyoneai/notebooks/main/customers_and_orders/data/orders.csv')
  with open('./sample_data/orders.csv', 'wb') as f:
    f.write(r.content)

import_data_files()
print("Customers and orders CSV files have been added './sample_data'")

from os.path import exists
import csv

# check if customers file can be found and open the file
datafile_customers = "./sample_data/customers.csv"
if not exists(datafile_customers):
  raise SystemExit("You should run the first code cell and download the dataset files!")

#counter for customers
customer_count = 0

# init to get the states and last names and the not repeated states
state_count = {}
lastname_count = {}
estados_unicos = set()

with open(datafile_customers, 'r') as fl:
    csv_customers_reader = csv.reader(fl, delimiter=',')

    # Skip the header
    next(csv_customers_reader)

    # we see all the states to count them
    for row in csv_customers_reader:
        #to know the amount of customers
        customer_count += 1
        #checking every state and lastname in the loop
        state = row[4]
        lastname = row[2]

        #adding to estados_unicos to avoid later repeated values
        estados_unicos.add(state)

        # Update the count for the different states and lastnames
        state_count[state] = state_count.get(state, 0) + 1
        lastname_count[lastname] = lastname_count.get(lastname, 0) + 1

print("Anwers about customers:")

# Find the maximum count of states
max_state = max(state_count, key=state_count.get, default=None)

#state minimum of customers
#find the min value
min_value_state = min(state_count.values(), default=None)
min_state = [key for key, value in state_count.items() if value == min_value_state]

#get the amount of states
max_count_states = state_count[max_state]

#get the quantity not repeated of states
cantidad_estados = len(estados_unicos) - 1

max_lastname = max(lastname_count, key=lastname_count.get)

#Answer 1
print(f"How many customers are in the file? {customer_count}")

#Answer 2
print(f"In how many different states do the customers live in? {cantidad_estados}")

#answer 3
print(f" What is the state with the most customers? {max_state}")

#answer 4
print(f" What is the state with the least customers? {min_state}")

#answer 5
print(f" What is the most common last name? {max_lastname}")


#Get customer names I do separately from the for from before to avoid iteration errors
with open(datafile_customers, 'r') as fl:
    csv_customers_reader_data = csv.reader(fl, delimiter=',')

    # Skip the header
    next(csv_customers_reader_data)

    #store customer names and id
    customer_names = {row[0]: f"{row[1]} {row[2]}" for row in csv_customers_reader_data}

# check if orders file can be found and open the file
datafile_orders = "./sample_data/orders.csv"
if not exists(datafile_orders):
  raise SystemExit("You should run the first code cell and download the dataset files!")

#to add up unique orders through the loop
unique_orders = set()

#count items and orders in csv
total_items = 0
total_orders = 0

#to count product in same order
order_product_count = {}

#create a counter for order_ids
order_id_counts = {}

#counter for oct 2021 orders
october2021_order_count = 0

#to calculate money spent per customer
customer_totals = {}

#to calculate monthly total sales
monthly_total_sales = defaultdict(float)

#to get max spender
max_spend = 0
customer_max_spender_id = 0

with open(datafile_orders, 'r') as fl:
    csv_orders_reader = csv.reader(fl, delimiter=',')

    # Skip the header
    next(csv_orders_reader)

    # we see all the states to count them
    for row in csv_orders_reader:
        #to know the amount of orders
        order_id = row[1] #order_id is the second column

        #check items
        product_name = row[4] #get the ProductName column to check if repeats of its different

        #to check for new orders in the same order_id
        key = (order_id, product_name)

        #update the count for this order and product combination
        order_product_count[key] = order_product_count.get(key, 0) + 1

        #count order_id
        order_id_counts[order_id] = order_id_counts.get(order_id, 0) + 1

        #check orders from October 2021 just checking the first 7 letters
        order_date_str = row[2][:7]

        #count months from orders
        month = row[2][5:7]

        #get total sales for order
        total_amount = float(row[3])

        monthly_total_sales[month] += total_amount

        #get year
        year = row[2][:4]

        #add totals to customer from order from 2021
        if year == "2021":
          #check customer id
          amount_spent = total_amount;
          customer_max_spender_id = row[0]
          customer_totals[customer_max_spender_id] = customer_totals.get(customer_max_spender_id, 0) + total_amount

        #if conditions met I add to the count of oct 21
        if order_date_str == "2021-10":
          october2021_order_count += 1

        #count total orders
        total_orders += 1

        #to avoid lates repetead values
        unique_orders.add(order_id)

#get the unique orders
num_unique_orders = len(unique_orders)

#calculate avergate of items per order
#get total unique products
total_items = sum(order_product_count.values())
average_items_per_order = round(total_items/num_unique_orders, 2)

#calculate max items per order
max_items_per_order = max(order_id_counts.values())

#calculate customer most spender
max_spender_id = max(customer_totals, key=customer_totals.get)
customer_spent_most = customer_names.get(max_spender_id, "John Doe") #john doe is just in case is wrong for some reason
# Sort the customer_totals dictionary by values in descending order
sorted_customers = sorted(customer_totals.items(), key=lambda x: x[1], reverse=True)

# Convert numeric months to month names
month_names = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

#calculate best month based on total sales per month
best_month_sales_number = int(max(monthly_total_sales, key = monthly_total_sales.get))
best_month_sales_name = month_names[best_month_sales_number]

print("\nAnwers about orders:")
#answer 1
print(f" How many unique orders are in the orders.csv file? {num_unique_orders}")

#anwer 2
print(f" What is the average number of items per order (rounded to two decimal places)? {average_items_per_order}") #quantity and product is not the same

#answer 3
print(f" What is the highest number of items per order? {max_items_per_order}")

#answer 4
print(f" What is the number of orders placed in October 2021? {october2021_order_count}")

#answer 5
print(f" Which customer spent the most amount of money in 2021? {customer_spent_most}")
# Print the top 10 customers and their spending values
for rank, (customer_id, spending) in enumerate(sorted_customers[:10], start=1):
    customer_rank_spent_most = customer_names.get(customer_id, "John Doe")
    print(f"   Rank {rank}: Customer {customer_rank_spent_most} spent {spending}")

#answer 6
print(f" Historically, what is the best month for sales? {best_month_sales_name}")
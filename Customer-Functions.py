import pandas as pd
import datetime
import numpy as np


my_dataFrame = pd.read_csv("OnlineRetail.csv", dtype={'CustomerID': object})
my_dataFrame["UnitPrice"] = my_dataFrame["UnitPrice"].str.replace(',','.')


#number of customers
def get_number_of_customers():

    no_of_customers = len(my_dataFrame["CustomerID"].unique())
    info = "Number of customers: " + str(no_of_customers)
    
    return info

#print(get_number_of_customers())


#number of purchases for each customer
def get_frequency_for_each_customer():

    frequency = my_dataFrame.groupby("CustomerID").size()
    frequency = frequency.sort_values(ascending=False).reset_index()
    
    return frequency

#print(get_frequency_for_each_customer())

    
#the last purchase for each customer
def get_recency_for_each_customer():
    
    my_dataFrame['InvoiceDate'] =  pd.to_datetime(my_dataFrame['InvoiceDate'])
    frequency = my_dataFrame.groupby("CustomerID")
    last_purchase = frequency['InvoiceDate'].max().reset_index()
    
    return last_purchase

#print(get_recency_for_each_customer())


#the first purchase for each customer
def get_lifetime_for_each_customer():

    my_dataFrame['InvoiceDate'] =  pd.to_datetime(my_dataFrame['InvoiceDate'])
    frequency = my_dataFrame.groupby("CustomerID")
    first_purchase = frequency['InvoiceDate'].min().reset_index()
    
    return first_purchase

#print(get_lifetime_for_each_customer())


#total money spent for each customer
def get_monetary_value():

    my_dataFrame["Total"] = my_dataFrame["Quantity"] * my_dataFrame["UnitPrice"].astype(float)

    monetary_value = my_dataFrame.groupby("CustomerID")["Total"].sum()
    monetary_value = monetary_value.sort_values(ascending=False).reset_index()

    return monetary_value

#print(get_monetary_value())


#the most money that each customer spent at once
def get_max_money_spent_for_each_customer():

    my_dataFrame["Total"] = my_dataFrame["Quantity"] * my_dataFrame["UnitPrice"].astype(float)
    maximal_values = my_dataFrame.groupby(["CustomerID","Country"])["Total"].max()
    maximal_values = maximal_values.sort_values(ascending=False).reset_index()

    return maximal_values

#print(get_max_money_spent_for_each_customer())


#the best customers (by number --> top 3 customers, to 5, top 10 ...)
def get_top_customers(number):

    top_customers = get_max_money_spent_for_each_customer()
    top_customers = top_customers.head(number)

    return top_customers

#print(get_top_customers(3))
#print(get_top_customers(10))


#the most valuable product that each customer bought, and its price
def get_most_valuable_product():
    
    most_valuable = my_dataFrame[["CustomerID", "Description", "UnitPrice"]].sort_values("UnitPrice", ascending=False).groupby("CustomerID").first()
    most_valuable = most_valuable.reset_index()
    most_valuable = most_valuable.sort_values("UnitPrice", ascending=False).reset_index(drop=True)
    
    return most_valuable

#print(get_most_valuable_product())


#the least valuable product that each customer bought, and its price
def get_least_valuable_product():

    least_valuable = my_dataFrame[["CustomerID", "Description", "UnitPrice"]].sort_values("UnitPrice", ascending=True).groupby("CustomerID").first()
    least_valuable = least_valuable.reset_index()
    least_valuable = least_valuable.sort_values("UnitPrice", ascending=True).reset_index(drop=True)

    return least_valuable

#print(get_least_valuable_product())
    

#best-selling products
def get_best_selling_products():

    best_product = my_dataFrame[["Description", "Quantity"]].groupby("Description")["Quantity"].sum(drop = True)
    best_product = best_product.reset_index()
    best_product = best_product.sort_values("Quantity", ascending = False).reset_index()
    
    return best_product

#print(get_best_selling_products())


#the least-selling product
def get_least_selling_products():
    
    least_product = my_dataFrame[["Description", "Quantity"]].groupby("Description")["Quantity"].sum()
    least_product = least_product.reset_index()
    least_product = least_product.sort_values("Quantity", ascending = True).reset_index(drop = True)
    
    return least_product

#print(get_least_selling_products())


#how many times each customer visits the website (in days)
def get_number_of_website_visits():
    
    my_dataFrame['InvoiceDate'] = pd.to_datetime(my_dataFrame['InvoiceDate']).dt.date
    site_visits = my_dataFrame[["CustomerID", "InvoiceDate"]].groupby("CustomerID")["InvoiceDate"].nunique().to_frame("No. of Visits [days]")
    site_visits = site_visits.sort_values("No. of Visits [days]", ascending=False).reset_index()
    
    return site_visits

#print(get_number_of_website_visits())


#full info for each customer
#(customer id, country, first purchase, last purchase, number of purchases, max spent, min spent, avrage spent, total spent)
def get_full_info_for_each_customer():

    my_dataFrame["Total"] = my_dataFrame["Quantity"] * my_dataFrame["UnitPrice"].astype(float)
    full_info = my_dataFrame.groupby("CustomerID")

    user = []
    country = []
    first_purchase = []
    last_purchase = []
    number_of_purchases = []
    total_spent = []

    full_info_dataFrame = pd.DataFrame()
    
    for key, data in full_info:

        user.append(data["CustomerID"].iloc[0])
        country.append(data["Country"].iloc[0])
        first_purchase.append(data['InvoiceDate'].min())
        last_purchase.append(data['InvoiceDate'].max())
        number_of_purchases.append(len(data))
        total_spent.append(data["Total"].sum())

        new_dataFrame = pd.DataFrame({"User": user,
                                        "Country": country,
                                        "First Buy": first_purchase,
                                        "Last Buy": last_purchase,
                                        "Purchases": number_of_purchases,
                                        "Total": total_spent})

        full_info_dataFrame =pd.concat([full_info_dataFrame, new_dataFrame], ignore_index = True)

    full_info_dataFrame = full_info_dataFrame.drop_duplicates()
    full_info_dataFrame = full_info_dataFrame.sort_values(["Country", "Total"], ascending = False).reset_index(drop = True)

    return full_info_dataFrame
        

#print(get_full_info_for_each_customer())


#full info for specific customer
#(customer id, country, first purchase, last purchase, number of purchases, max spent, min spent, avrage spent, total spent)
def get_full_info_for_each_customer(customerid):
    
    my_dataFrame["Total"] = my_dataFrame["Quantity"] * my_dataFrame["UnitPrice"].astype(float)
    specific_customer = my_dataFrame[my_dataFrame["CustomerID"] == str(customerid)]
    
    full_info_dataFrame = pd.DataFrame({"User": [specific_customer["CustomerID"].iloc[0]],
                                        "Country": [specific_customer["Country"].iloc[0]],
                                        "First Buy": [specific_customer['InvoiceDate'].min()],
                                        "Last Buy":  [specific_customer['InvoiceDate'].max()],
                                        "Purchases": [len(specific_customer)],
                                        "Total": [specific_customer["Total"].sum()]})

    return full_info_dataFrame
        
#print(get_full_info_for_each_customer(18102))

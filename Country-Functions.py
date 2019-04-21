import pandas as pd
import datetime
import numpy as np


my_dataFrame = pd.read_csv("OnlineRetailNEW.csv", dtype={'CustomerID': object})
my_dataFrame["UnitPrice"] = my_dataFrame["UnitPrice"].str.replace(',','.')


#number of purchases for each country
def get_purchases_no_by_country():

    no_of_purchases = my_dataFrame.groupby("Country").size().to_frame("No. of Purchases")
    no_of_purchases = no_of_purchases.sort_values("No. of Purchases", ascending = False).reset_index()
    
    return no_of_purchases

#print(get_purchases_no_by_country())


#number of diferent customers by country
def get_customers_no_by_country():

    no_of_customers = my_dataFrame[["Country", "CustomerID"]].groupby("Country")["CustomerID"].nunique().to_frame("No. of Customers")
    no_of_customers = no_of_customers.sort_values("No. of Customers", ascending = False).reset_index()
    
    return no_of_customers

#print(get_customers_no_by_country())   


#number of diferent products sold in each country
def get_products_no_by_country():

    no_of_products = my_dataFrame[["Country", "Description"]].groupby("Country")["Description"].nunique().to_frame("No. of Products")
    no_of_products = no_of_products.sort_values("No. of Products", ascending = False).reset_index()
    
    return no_of_products

#print(get_products_no_by_country())   


#total earned money by every country
def get_total_money_by_country():

    my_dataFrame["Total"] = my_dataFrame["Quantity"] * my_dataFrame["UnitPrice"].astype(float)

    country_money = my_dataFrame.groupby("Country")["Total"].sum()
    country_money = country_money.sort_values(ascending=False).reset_index()

    return country_money

#print(get_total_money_by_country())


def get_the_best_customer_for_each_country():

    best_customer = get_max_money_spent_for_each_customer()
    best_customer = best_customer[["Country", "CustomerID", "Total"]].groupby("Country").first()
    best_customer = best_customer.sort_values("Total", ascending=False).reset_index()

    return best_customer

#print(get_the_best_customer_for_each_country())

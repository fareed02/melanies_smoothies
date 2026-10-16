

import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"), col("SEARCH_ON"))
pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)

ingredients_list = st.multiselect("Choose up to 5 ingredients:", pd_df["FRUIT_NAME"].tolist(), max_selections=5)

if ingredients_list:
    ingredients_string = ""
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + " "
        search_on = pd_df.loc[pd_df["FRUIT_NAME"] == fruit_chosen, "SEARCH_ON"].iloc[0]
        st.write("The search value for", fruit_chosen, "is", search_on, ".")
        st.subheader(fruit_chosen + " Nutrition Information")
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on, timeout=10)
        if smoothiefroot_response.status_code == 200:
            st.json(smoothiefroot_response.json())
        else:
            st.write("Nutrition information is currently unavailable.")

    if st.button("Submit Order"):
        if name_on_order.strip():
            session.sql("INSERT INTO smoothies.public.orders (ingredients, name_on_order) VALUES (?, ?)", params=[ingredients_string.strip(), name_on_order]).collect()
            st.success("Your Smoothie is ordered for " + name_on_order + "!", icon="✅")
        else:
            st.warning("Please enter your name before submitting.")

if ingredients_list:
    ingredients_string = ''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

        

    my_insert_stmt = """INSERT INTO smoothies.public.orders(ingredients, name_on_order) VALUES ('""" + ingredients_string + """', '""" + name_on_order + """')"""
    # st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered for ' + name_on_order + '!', icon="✅")

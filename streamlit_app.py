# Import python packages
import streamlit as st
import requests
import pandas as pd
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col




# Write directly to the app
st.title(":cup_with_straw Customize Your Smoothie! :cup_with_straw")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)


#session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"), col("SEARCH_ON"))
# st.dataframe(data=my_dataframe, use_container_width=True)

#Convert the snowpark dataframe to a pandas Dataframe so we can use the LOC function
pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)



ingredient_list= st.multiselect("Choose up to 5 ingredients:", my_dataframe, max_selections=5)




if ingredient_list:
    ingredient_string = ''
    for each_item in ingredient_list:
        ingredient_string += each_item + ' '
        st.subheader(each_item + 'Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + each_item)
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                values ('""" + ingredient_string + """','""" + name_on_order + """')
                """
    
    # st.write(my_insert_stmt)

    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")









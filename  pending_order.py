# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col, when_matched




# Write directly to the app
st.title(":Pending Smoothie Order :cup_with_straw")
st.write(
    """Order that need to filled:
    """
)

session = get_active_session()

my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()

if my_dataframe:
    editable_df = st.data_editor(my_dataframe)
    
    
    submitted = st.button('Submit')
    
    if submitted:
    
        try:       
            og_dataset = session.table("smoothies.public.orders")
            edited_dataset = session.create_dataframe(editable_df)
            og_dataset.merge(edited_dataset
                             , (og_dataset['order_uid'] == edited_dataset['order_uid'])
                             , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                            )
            st.success('Order(s) is Upadate!', icon='👍')
    
        except:
            st.success('Something went wrong!')
else:
    st.success('All orders is filleds!')
        







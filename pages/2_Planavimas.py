import streamlit as st
import pandas as pd


# Create an empty dataframe with the required columns
columns = ['Name', 'Production', 'Net_price', 'Sub_price', 'Total_price']

# Initialize an empty DataFrame
df = pd.DataFrame(columns=columns)

product_name_list = sorted(list(st.session_state.get("get_products", "Value not set")["Produktas"]))
product_dataframe = st.session_state.get("product_list", "Value not set")
print(product_dataframe)


def planavimas():
    st.title("Production Data Entry")
    
    # Display the editable table with st.data_editor
    st.subheader("Edit Production Data:")
    edited_df = st.data_editor(df,num_rows="dynamic",use_container_width=True, column_config={
        'Name': st.column_config.SelectboxColumn('Gaminys',options=product_name_list,required=True),
        'Production': st.column_config.NumberColumn('Gaminamas kiekis', min_value=1),
        'Net_price': st.column_config.NumberColumn('Net_price', min_value=0.0,required=True,disabled=True),
        'Sub_price': st.column_config.NumberColumn('Sub_price', min_value=0.0,required=True,disabled=True),
        'Total_price': st.column_config.NumberColumn('Total_price', min_value=0.0,required=True,disabled=True)
    })



    # Create four columns with equal width
    col1, col2, col3, col4 = st.columns(4,gap="small")

    with col1:
        st.button(label="Paskačuoti savikaina",)

    with col2:
        st.form("1")

    with col3:
        st.form("2")

    with col4:
        st.form("3")


    # Button to add data to the Excel file
    if st.button("Add to production"):
        if not edited_df.empty:
            try:
                # Read the existing data from the Excel file
                existing_data = pd.read_excel("production_data.xlsx")
                # Append the new data
                combined_data = pd.concat([existing_data, edited_df], ignore_index=True)
            except FileNotFoundError:
                # If the file doesn't exist, start with the current data
                combined_data = edited_df
            
            # Save to the Excel file
            combined_data.to_excel("production_data.xlsx", index=False)
            st.success("Data saved to production_data.xlsx")
        else:
            st.error("No data to save.")

if __name__ == "__main__":
    planavimas()
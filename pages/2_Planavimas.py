import streamlit as st
import pandas as pd

# Create an empty dataframe with the required columns
columns = ['Name', 'Production', 'Net_price', 'Sub_price', 'Total_price']
df = pd.DataFrame(columns=columns)



def planavimas():

    st.title("Production Data Entry")
    
    # Display the empty dataframe as a table in the app
    st.dataframe(df)

    # Create input fields for the user to enter data
    name = st.text_input("Name")
    production = st.number_input("Production", min_value=0)
    net_price = st.number_input("Net_price", min_value=0.0, format="%.2f")
    sub_price = st.number_input("Sub_price", min_value=0.0, format="%.2f")
    total_price = st.number_input("Total_price", min_value=0.0, format="%.2f")

    # Button to add data to the table
    if st.button("Add to production"):
        if name and production > 0 and net_price > 0 and sub_price > 0 and total_price > 0:
            # Append the new data to the dataframe
            new_data = {
                'Name': name,
                'Production': production,
                'Net_price': net_price,
                'Sub_price': sub_price,
                'Total_price': total_price
            }
            df.loc[len(df)] = new_data
            st.success("Data added to the table!")
        else:
            st.error("Please fill in all the fields correctly.")

    # Button to save the dataframe to an Excel file
    if st.button("Save to Excel"):
        # Specify the Excel file name
        file_name = "production_data.xlsx"

        # Check if the file already exists
        try:
            # Try reading the existing data
            existing_data = pd.read_excel(file_name)
            # Append the new data to the existing data
            combined_data = pd.concat([existing_data, df], ignore_index=True)
        except FileNotFoundError:
            # If the file doesn't exist, just use the current df
            combined_data = df

        # Save the combined data to the Excel file
        combined_data.to_excel(file_name, index=False)
        st.success(f"Data saved to {file_name}")

if __name__ == "__main__":
    planavimas()
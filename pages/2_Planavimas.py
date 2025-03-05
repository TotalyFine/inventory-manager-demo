import streamlit as st
import pandas as pd


product_name_list = sorted(list(st.session_state.get("get_products", "Value not set")["Produktas"]))
product_dataframe = st.session_state.get("product_list", "Value not set")


def get_Ingridients():
    product_xlsx = pd.ExcelFile("./Files/products.xlsx")
    product_sheetnames = list(product_xlsx.sheet_names)
    product_list = {}
    data_list = []
    for sheet in product_sheetnames:
        data = product_xlsx.parse(sheet)
        new_data_columns = list(data[data["Category"].isin(["Discription","Ingredient"])]["Type"])
        new_data_values = list(data[data["Category"].isin(["Discription","Ingredient"])]["Value"])
        dict_data = dict(zip(new_data_columns,new_data_values))
        data_list.append(dict_data)
    product_list = pd.DataFrame(data_list)
    return product_list


def fill_get_netprice(row):
    value = product_dataframe[product_dataframe["Produktas"] == row[0]]["Savikaina"].values[0]
    return value

def fill_get_price(row):
    value = product_dataframe[product_dataframe["Produktas"] == row[0]]["Kaina"].values[0]
    return value


def planavimas(): ############################ MAIN WINDOW ###################################
    st.title("Planavimas")

    # Create an initial DataFrame with the columns
    columns = ['Name', 'Production', 'sell_price', 'net_price', 'magrin']
    df = pd.DataFrame(columns=columns)

    st.write("Galima įterpti neribotą kiekį elučių. Reikia pasirinkti gaminio pavadinimą kurį norima pagaminti ir įveti norima pagaminti kiekį kilogramais")
    edited_df = st.data_editor(df, num_rows="dynamic", key="data_editor",column_order=['Name', 'Production'],column_config={
        'Name': st.column_config.SelectboxColumn('Gaminys',options=product_name_list,required=True,width="large"),
        'Production': st.column_config.NumberColumn('Gaminamas kiekis', min_value=1,width="medium")
    })
    #Calculations
    if not edited_df.empty:
        edited_df["Production"] = edited_df["Production"] * 0.85
        edited_df["sell_price"] = edited_df.apply(fill_get_price,axis=1) * edited_df['Production']
        edited_df["net_price"] = 1.05 * edited_df['Production'] * edited_df.apply(fill_get_netprice,axis=1)
        edited_df["magrin"] = (edited_df["sell_price"] -  edited_df["net_price"]) / edited_df["sell_price"]

    st.subheader("Skaičiavimai",divider="orange")
    st.write("""#### Bedros sumos ir marža
- Gaminamas kiekis: bendras gaminamas kiekis su 85% išeiga
- Pardavimo suma: pardavimo kaina vieno kg * gaminamas kiekis
- Bendra savikaina: 1kg savikaina * gaminamas kiekis * 5% (kitos išlaidos)
- Marža: Pardavimo suma - Bendra savikaina
                """)
    
    
    st.dataframe(edited_df,use_container_width=True, hide_index=True, column_config={
        'Name': st.column_config.SelectboxColumn('Gaminys',options=product_name_list,required=True),
        'Production': st.column_config.NumberColumn('Pagaminto produkto kg', min_value=1),
        'sell_price': st.column_config.NumberColumn('Pardavimo suma ',format=" %.2f €"),
        'net_price': st.column_config.NumberColumn('Bendra savikaina',format=" %.2f €"),
        'magrin': st.column_config.NumberColumn('Marža %',format="%.2f %%")
    })
    
    ##########################################################
    st.subheader("Žaliavų skaičiavimai",divider="orange")

    # Example data (replace with your own data)
    df_products = edited_df

    df_ingredients = get_Ingridients()

    # Merge on the product name
    merged = pd.merge(df_products, df_ingredients, how="left",left_on="Name",right_on="Produktas")
    

    # Multiply each ingredient fraction by the product quantity
    ingredient_cols = df_ingredients.columns.drop(['Produktas','Pavadinimas'])
    for col in ingredient_cols:
        merged[col] = merged[col] * merged['Production']
    
    # Sum the total amounts needed for each ingredient
    total_ingredients = merged[ingredient_cols].sum().reset_index()
    total_ingredients.columns = ['Ingridientas', 'Iš viso bus panaudota kg']

    total_ingredients

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
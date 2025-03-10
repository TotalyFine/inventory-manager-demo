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

    st.write("Galima įterpti neribotą kiekį eilučių. Pasirinkite gaminio pavadinimą ir įveskite gaminamą kiekį kilogramais.")
    edited_df = st.data_editor(df, num_rows="dynamic", key="data_editor",column_order=['Name', 'Production'],column_config={
        'Name': st.column_config.SelectboxColumn('Gaminys',options=product_name_list,required=True,width="large"),
        'Production': st.column_config.NumberColumn('Gaminamas kiekis, kg', min_value=1,width="medium")
    })
    #Calculations
    if not edited_df.empty:
        edited_df["Production"] = edited_df["Production"] * 0.85
        edited_df["sell_price"] = edited_df.apply(fill_get_price,axis=1) * edited_df['Production']
        edited_df["net_price"] = edited_df['Production'] * edited_df.apply(fill_get_netprice,axis=1) * 1.05
        edited_df["magrin"] = (edited_df["sell_price"] -  edited_df["net_price"]) / edited_df["sell_price"]

    st.subheader("Skaičiavimai",divider="orange")
    st.write("""#### Bedros sumos ir marža
- Gaminamas kiekis = bendras gaminamas kiekis su 85% išeiga
- Pardavimo suma = 1kg gaminio pardavimo kaina * gaminamas kiekis
- Bendra savikaina = 1kg gaminio savikaina * gaminamas kiekis + 5% (kitos sąnaudos nuo bendros sumos)
- Marža = marža %
                """)
    
    
    st.dataframe(edited_df,use_container_width=True, hide_index=True, column_config={
        'Name': st.column_config.SelectboxColumn('Gaminys',options=product_name_list,required=True,width="large"),
        'Production': st.column_config.NumberColumn('Pagaminto produkto kg', min_value=1,width="small"),
        'sell_price': st.column_config.NumberColumn('Pardavimo suma ',format=" %.2f €",width="small"),
        'net_price': st.column_config.NumberColumn('Bendra savikaina',format=" %.2f €",width="small"),
        'magrin': st.column_config.NumberColumn('Marža %',format="%.2f %%",width="small")
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
    total_ingredients.columns = ['Ingridientas', 'kg']
    st.write("Reikalingas bendras žaliavų kiekis kilogramais")
    st.dataframe(total_ingredients.sort_values(by="kg",ascending=False),hide_index=True, width=500)



    #################### 
    st.subheader("Perkelti į gamybą",divider="orange")
    # Button to add data to the Excel file


    col1, col2 = st.columns(2,gap="small",vertical_alignment="bottom")
    
    with col1:
        production_date = st.date_input("Gaminimo data",format="YYYY-MM-DD")

    data_to_production = edited_df.drop(['sell_price', 'net_price', 'magrin'], axis=1)
    data_to_production["Data"] = production_date
    data_to_production["Pagaminta"] = False
    data_to_production = data_to_production[["Data","Name","Production","Pagaminta"]]
    data_to_production = data_to_production.rename(columns={"Name": "Pavadinimas","Production": "Gaminamas kiekis"})

    with col2:
        if st.button("Gaminti",):
            if not data_to_production.empty:
                try:
                    # Read the existing data from the Excel file
                    existing_data = pd.read_excel("./Files/production_data.xlsx")
                    # Append the new data
                    combined_data = pd.concat([existing_data, data_to_production], ignore_index=True)
                except FileNotFoundError:
                    # If the file doesn't exist, start with the current data
                    combined_data = data_to_production
                
                # Save to the Excel file

                combined_data.to_excel("./Files/production_data.xlsx", index=False)
                st.success("Produktai perkelti į gamybą")
            else:
                st.error("Lentlė tusčia")
    st.write("Kas bus perkelta į gamybą:")
    st.dataframe(data_to_production,hide_index=True)

if __name__ == "__main__":
    planavimas()
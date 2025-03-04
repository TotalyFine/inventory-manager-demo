import streamlit as st
import pandas as pd

def products():

    def get_products():
        product_xlsx = pd.ExcelFile("./Files/products.xlsx")
        product_sheetnames = list(product_xlsx.sheet_names)
        product_list = {}
        data_list = []
        for sheet in product_sheetnames:
            data = product_xlsx.parse(sheet)
            new_data_columns = list(data[data["Category"].isin(["Discription","specification"])]["Type"])
            new_data_values = list(data[data["Category"].isin(["Discription","specification"])]["Value"])
            dict_data = dict(zip(new_data_columns,new_data_values))
            data_list.append(dict_data)
        product_list = pd.DataFrame(data_list)
        return product_list

    def get_material_prices():
        prices = pd.read_excel("./Files/raw materials.xlsx")
        return prices

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

    def get_ingridieant_price(product):
        get_ing = ingridients[ingridients["Produktas"] == product].dropna(axis=1).T
        get_ing.reset_index(inplace=True)
        get_ing.columns = ['Name', 'Value']
        # print(list(raw_material_prices["product"]))
        item_list = get_ing["Name"].values
        rawmaterial_list = list(raw_material_prices["product"])
        total_product_cost = 0
        for item in item_list:
            if item in rawmaterial_list:
                price = raw_material_prices[raw_material_prices["product"] == item].values[0][1]
                usage = get_ing[get_ing["Name"] == item].values[0][1]
                total_product_cost += price*usage
        #         print(f"Item: {item}, price {price}, usage {usage}")
        #         print(f"Total {item} price: {price*usage}")
        # print(f"Total {product} cost: {total_product_cost}")
        return total_product_cost

    product_list = get_products() 
    raw_material_prices = get_material_prices() 
    ingridients = get_Ingridients()

    # Calculate 
    product_list['Savikaina'] = product_list["Produktas"].apply(get_ingridieant_price)


    # ------------ Display Content -----------------------------------------------------------------
    st.write("# Duomenų Bazė: Gaminiai ir jų sudėtys")
    st.text("Visi duomenys yra kas kart iš naujo importojami iš xlsx lentelių")
    st.subheader("Products", divider="orange") 
    st.data_editor(
        product_list,hide_index=True,
        column_config={"Kaina":st.column_config.NumberColumn("Kaina 1kg",format=" %.2f €"),"Savikaina":st.column_config.NumberColumn("Savikaina 1kg",format=" %.2f €")}
    )


    st.subheader("Žaliavų kainos (€ / 1kg)", divider="orange")
    st.data_editor(raw_material_prices, width=500,hide_index=True,
        column_config={"price":st.column_config.NumberColumn("Kaina 1kg",format="%.2f €"),
                       "product":"Pavadinimas"}
    )


    st.subheader("Gaminio receptūra (pagaminti 1kg produkto)", divider="orange") 
    option = st.selectbox(label="Pasirinkt gaminį",options=list(ingridients["Produktas"]))

    dataframe = ingridients[ingridients["Produktas"] == option].dropna(axis=1).T
    dataframe.reset_index(inplace=True)
    dataframe.columns = ['Name', 'Value']

    st.table(dataframe)

if __name__ == "__main__":
    products()
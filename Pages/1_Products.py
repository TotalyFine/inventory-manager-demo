import streamlit as st
import pandas as pd

def app():
    st.set_page_config(
        page_title="Products",
        layout="wide",
        initial_sidebar_state="expanded"
    )

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

    def get_ingridieant_price(product,extra):
        get_ing = ingridients[ingridients["Produktas"] == product].dropna(axis=1).T
        get_ing.reset_index(inplace=True)
        get_ing.columns = ['Name', 'Value']
        print(get_ing["Name"])
        #get_ing


    
    
    

    product_list = get_products()
    raw_material_prices = get_material_prices()
    ingridients = get_Ingridients()
    price_test = get_ingridieant_price("Kiaulienos šašlykas",0)
    price_test

    # ------------ Display Content -----------------------------------------------------------------
    st.write("# Database: Products and raw material prices")
    st.subheader("Products", divider="orange") 
    st.data_editor(
        product_list,
        column_config={"Kaina":st.column_config.NumberColumn("Price 1kg",format=" %.2f €")}
    )

    st.subheader("Raw material prices (€ / 1kg)", divider="orange")
    st.data_editor(raw_material_prices, width=500,
        column_config={"price":st.column_config.NumberColumn("Price 1kg",format="%.2f €",)}
    )
    

    st.subheader("Product ingridients (To make 1kg product)", divider="orange") 
    option = st.selectbox(label="Select product to check ingridients",options=list(ingridients["Produktas"]))
    
    dataframe = ingridients[ingridients["Produktas"] == option].dropna(axis=1).T
    dataframe.reset_index(inplace=True)
    dataframe.columns = ['Name', 'Value']

    st.data_editor(dataframe, width=500)
    




    # for item in range(len(one_product_values)):
    #     if one_product_values[item] is not "nan":
            #print(one_product_columns[item],one_product_values[item])
     


    st.subheader("Full ingridients list ", divider="orange") 
    st.data_editor(ingridients)
    


if __name__ == "__main__":
    app()
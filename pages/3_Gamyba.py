import streamlit as st
import pandas as pd



def gamyba():
    st.title("Gamyba")
    st.write("""
Atlikus bet kokius pakeitimus lentelėje reikia paspausti mygtuką 'Išsaugoti', kad pakeitimai išsisaugotų į Excel failą. 
Data nurodo kada produktas buvo pridėtas į gamybą. 
Uždėjus varnelę ant “Pagaminta” ir išsaugojus pakeitimus, po puslapio atnaujinimo dings iš sąrašo ir atsiras puslapyje “Istorija”
""")
    
    
    EXCEL_FILE = "./Files/production_data.xlsx"



    def load_data():
        df = pd.read_excel(EXCEL_FILE)
        # Create a unique identifier column if one doesn't exist already
        df = df.reset_index().rename(columns={'index': 'Eilutė'})
        return df

    # Load full data


    df = load_data()
    df["Eilutė"] = df["Eilutė"] + 2

    # Apply your filter (e.g., only show rows where "completed" is False)
    filtered_df = df[df["Pagaminta"] == False]

    col1,col2,col3 = st.columns(3,vertical_alignment="bottom")

    with col1:
        list_of_products =df["Pavadinimas"].unique()
        filter_product = st.selectbox("Filtruoti įrašus paga pavadinima", options=list_of_products,index=None)  
        if filter_product != None:
            filtered_df = filtered_df[filtered_df["Pavadinimas"] == filter_product]

    with col2:
        pass

    with col3:
        pass
        
    

    



    # Show editable table for the filtered data
    edited_filtered_df = st.data_editor(data=filtered_df, num_rows="dynamic",hide_index=True,column_config={
        "Data": st.column_config.DatetimeColumn(format="YYYY MM DD")
    })

    if st.button("Išsaugoti"):
        # Loop through edited rows and update the corresponding rows in the full dataframe
        for _, edited_row in edited_filtered_df.iterrows():
            orig_idx = edited_row["Eilutė"]
            # Update each column individually in the original dataframe
            for col in edited_filtered_df.columns:
                df.loc[df["Eilutė"] == orig_idx, col] = edited_row[col]

        # Save the full updated DataFrame back to Excel (dropping the helper column if desired)
        df.drop(columns=["Eilutė"]).to_excel(EXCEL_FILE, index=False)
        st.success("Excel file updated successfully!")


if __name__ == "__main__":
    gamyba()





    
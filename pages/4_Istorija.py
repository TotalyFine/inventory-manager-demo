import streamlit as st
import pandas as pd



def istorija():
    st.title("Istorija")

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
    filtered_df = df[df["Pagaminta"] == True]

    # Show editable table for the filtered data
    edited_filtered_df = st.data_editor(data=filtered_df, num_rows="dynamic",hide_index=True)

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
    istorija()





    
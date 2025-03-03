import streamlit as st

def info():
    st.write("""
# Gamybos planavimas: pavyzdys
Čia yra pagrindinis puslapis. Galima atvaizduoti bet kokią informaciją lentelės, diagramos ar teksto pavidalu. Pvz.: paskutinės 5 pagamintų prekių arba paskutinės įtrauktos į gamybą.
Kairėje yra menu. Galima kiekvieną funkciją išskaidyti į atskirus puslapius. Trumpai apie kiekvieną iš puslapių:

""")
    
    st.write("### Gaminiai")
    st.write("Visa informacija susijusi su gaminiais. Gaminių ir ingredientų sąrašas. Gaminių savikainos paskaičiuotos pagal nustatytas kainas kurios yra taip pat paimtos iš Excel failų")
    

def app():
    st.set_page_config(page_title="Pagrindinis",layout="wide", initial_sidebar_state="expanded")
    info()

if __name__ == "__main__":
    app()




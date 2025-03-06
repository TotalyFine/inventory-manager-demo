import streamlit as st

def info():
    st.write("""
# Gamybos planavimas: pavyzdys
Čia yra pagrindinis puslapis. Galima atvaizduoti bet kokią informaciją: lentelės, diagramos ar teksto pavidalu. Pvz.: paskutinių 5 pagamintų prekių arba paskutinių įtrauktų į gamybą.
Kairėje yra meniu. Galima kiekvieną funkciją išskaidyti į atskirus puslapius. Trumpai apie kiekvieną iš puslapių:

""")
    
    st.write("### Produkcija")
    st.write("Visa informacija susijusi su produkcija. Gaminių ir ingredientų sąrašas. Gaminių savikainos paskaičiuotos pagal nustatytas kainas kurios yra taip pat paimtos iš Excel failų")

    st.write("### Planavimas")
    st.write("Gaminių pridėjimas į gamybą. Žaliavų sąnaudų apskaičiavimas.")

    st.write("### Gamyba ir Istorija ")
    st.write("Visa informacija yra paimta iš to paties failo ir atvaziuojama skirtinguose puslapiuose. Yra importuota virš 5 000 eilučių ir nestringa. ")
    st.write("Pagaminti produktai atvaizduojami 'Gamyba' puslapyje o pagaminti 'istorija'")

    st.write("### Demo")
    st.write("demonstracinis puslapis su diagramomis")

 

def app():
    st.set_page_config(page_title="Pagrindinis",layout="wide", initial_sidebar_state="expanded")
    info()

if __name__ == "__main__":
    app()




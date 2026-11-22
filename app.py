import streamlit as st

st.set_page_config("Manhwaverse")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    
if "user" not in st.session_state:
    st.session_state.user = None
    
if "edit" not in st.session_state:
    st.session_state.edit = False
    

if st.session_state.logged_in == True and st.session_state.edit == False:
    pg = st.navigation([
        st.Page("pages/beranda.py", default=True),
        st.Page("pages/Cari_Manhwa.py"),
        st.Page("pages/Statistik.py"),
        st.Page("pages/Pengaturan.py")
    ])
    
    pg.run()
    
elif st.session_state.logged_in == True and st.session_state.edit == True:
    pg = st.navigation([
        st.Page("pages/Edit_Status.py")
    ], position="hidden")
    
    pg.run()

else:
    pg = st.navigation([
        st.Page("pages/login.py", title="Login", default=True),
        st.Page("pages/register.py", title="Register")
    ], position="hidden")
    pg.run()
    

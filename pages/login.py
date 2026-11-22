import streamlit as st 
from database import supabase


with st.container(vertical_alignment='center', border=True):
    st.subheader("Login", text_alignment='center')
    username = st.text_input("Masukkan Username: ", placeholder="Username", required=True).strip()
    password = st.text_input("Masukkan Password: ", placeholder="Password", type="password", required=True).strip()
    
    
    if st.button("Login", use_container_width=True):
        cek_user = (supabase.table("User").select("username", "password").eq("username", username).execute())
        if len(cek_user.data) == 0:
            st.warning("Username belum ada. Buat akun dulu.")
        else:
            passDb = cek_user.data[0]["password"]
            if password == passDb:
                st.session_state.logged_in = True
                st.session_state.user = username
            else:
                st.warning("Password Salah!")
        st.rerun()
    
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.page_link("pages/register.py", label="Belum Punya Akun? Buat Akun")
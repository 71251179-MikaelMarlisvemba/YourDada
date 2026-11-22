import streamlit as st 
from database import supabase


with st.container(border=True):
    st.subheader("Buat Akun", text_alignment='center')
    username = st.text_input("Masukkan Username: ", placeholder="Username", required=True).strip()
    password = st.text_input("Masukkan Password: ", placeholder="Password", type="password", required=True).strip()
    konfirmasi = st.text_input("Konfirmasi Password: ", placeholder="Password", type="password",required=True).strip()

    # submitted = st.form_submit_button("Buat Akun", use_container_width=True)

    if st.button("Buat Akun", use_container_width=True):
        cek = (supabase.table("User").select("username").ilike("username", username).execute())
        
        if len(cek.data) > 0:
            st.warning("Username sudah digunakan!")
        elif len(username) == 0:
            st.warning("Username Wajib diisi!")
        elif len(username) <= 3:
            st.warning("Username Minimal 4 karakter!")
        elif len(password) < 8:
            st.warning("Panjang password minimal 8")
        elif password != konfirmasi:
            st.warning("Password tidak sama!")
        else:
            response = (supabase.table("User").insert({
                "username" : username,
                "password" : password
            }).execute())
            st.success("Berhasil membuat akun!")
            
        st.switch_page("pages/login.py")
            
        
    st.page_link("pages/login.py", label="Sudah Punya Akun? Login")
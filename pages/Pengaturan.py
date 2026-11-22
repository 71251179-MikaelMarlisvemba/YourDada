import streamlit as st 
from database import supabase
        
st.header("Pengaturan")

with st.container(border=True, vertical_alignment="center"):
    st.subheader("Ganti Password")
    pw_lama = st.text_input("**Password Lama**", placeholder="Masukkan password lama", type="password", required=True).strip()
    pw_baru = st.text_input("**Password Baru**", placeholder="Masukkan password baru", type="password", required=True).strip()
    konfirmasi = st.text_input("**Konfirmasi Password Baru**", placeholder="Ulangi password baru",type="password", required=True).strip()
    
    if st.button("Ganti Password"):
        cek_user = (supabase.table("User").select("username", "password").eq("username", st.session_state.user).execute())
        pw_db = cek_user.data[0]["password"]
        
        if pw_lama != pw_db:
            st.warning("Password Salah. Coba lagi!")
        elif len(pw_baru) < 8:
            st.warning("Panjang password minimal 8")
        elif pw_baru != konfirmasi:
            st.warning("Password Tidak Sama!")
        else:
            ubah = (supabase.table("User").update({"password" : pw_baru}).eq("username", st.session_state.user).execute())
            st.success("Berhasil ubah password!")
            
with st.container(border=True):
    st.subheader("Export Data")
    st.caption("Unduh koleksi manhwa Anda")
    col1, col2 = st.columns([0.1, 0.5])
    
    with col1:
        st.button("Export JSON")
        
    with col2:
        st.button("Export Excel")
            
if st.button("**Log Out**", type="primary", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.user = None
    st.rerun()
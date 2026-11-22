import streamlit as st
from database import supabase

st.header("Edit Status")
manhwa = st.session_state.edit_manhwa

col1, col2, col3 = st.columns([1,2,1])
with col2:
    with st.container(border=True, width="content"):
        cover = manhwa["cover"]
        judul = manhwa["judul_manhwa"]
        genre = manhwa["genre"]
        status = manhwa["status"]
        chapter = manhwa["chapter_terakhir"]
        
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.image(cover)
        
        st.write(f"**{judul}**")
        st.caption(genre)
        st.caption(f"Status: {status}")
        if status == "Ongoing":
            st.caption(f"Chapter Terakhir: {chapter}")
    
status_awal = manhwa["status"]
options = ["Belum Dibaca", "Ongoing", "Selesai Baca"]

status = st.selectbox("Status", options=options, index=options.index(status_awal))

if status == "Ongoing":
    chapter = st.number_input("Masukkan Chapter Terakhir : ", 1, value=manhwa["chapter_terakhir"])

col1, col2, col3 = st.columns([1, 2, 6], gap="xsmall")
with col1:
    if st.button("Selesai", type="primary"):
        ubah = (supabase.table("bookmark_user").update({"status" : status, "chapter_terakhir" : chapter}).eq("id_manhwa", manhwa["id_manhwa"]).execute())
        
        if ubah:
            st.session_state.edit = False
            st.rerun()
        else:
            st.error("Gagal menedit status!")

with col2:
    if st.button("Batal"):
        st.session_state.edit = False
        st.rerun()
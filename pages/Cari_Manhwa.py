import streamlit as st
from database import supabase
from manhwa import cari_manhwa
from datetime import datetime
from zoneinfo import ZoneInfo
import random as rand

st.header("Cari Manhwa")

cari = st.text_input("**Cari**", placeholder="Masukkan nama manhwa").strip()

genres = [
    "Semua",
    "Action",
    "Adventure",
    "Comedy",
    "Drama",
    "Fantasy",
    "Romance",
    "Horror",
    "Mystery",
    "Psychological",
    "Slice of Life",
    "Sports",
    "Supernatural",
    "Thriller"
]

user = (supabase.table("User").select("id_user").eq("username", st.session_state.user).execute())
id_user = user.data[0]["id_user"]

data_user = (supabase.table("bookmark_user").select("judul_manhwa").eq("id_user", id_user).execute())
data_manhwa = [item["judul_manhwa"] for item in data_user.data]

genre = st.selectbox("**Filter Kategori**", options=genres)

if "hasil_manhwa" not in st.session_state:
    st.session_state.hasil_manhwa = []
    
if "page" not in st.session_state:
    st.session_state.page = 1
    
if "jumlah" not in st.session_state:
    st.session_state.jumlah = 0

def muat_manhwa():
    st.session_state.hasil_manhwa = cari_manhwa(
            search=st.session_state.manhwa,
            genre=st.session_state.genre,
            page=st.session_state.page
        )

if st.button("**Cari**", use_container_width=True):
    st.session_state.manhwa = cari
    st.session_state.genre = genre
    muat_manhwa()
    
      
hasil = st.session_state.hasil_manhwa
st.session_state.jumlah = len(hasil)

col1, col2 = st.columns(2)
if col1.button("Sebelumnya", disabled=st.session_state.page == 1, use_container_width=True):
    st.session_state.page -= 1
    muat_manhwa()
    st.rerun()
            
if col2.button("Selanjutnya", disabled=st.session_state.jumlah < 18, use_container_width=True):
    st.session_state.page += 1
    muat_manhwa()
    st.rerun()

if len(hasil) == 0:
    st.subheader("Hasil Pencarian: ")
            
else:
    st.subheader(f"Hasil Pencarian (Page {st.session_state.page}): ")
    cols = st.columns(3)
    
    for index, manga in enumerate(hasil):
        with cols[index % 3]:
            with st.container(border=True):
                cover = manga["coverImage"]["large"]
                
                st.image(cover,use_container_width=True)
                
                judul = (manga["title"]["english"] or manga["title"]["romaji"])
                
                st.markdown(f"**{judul}**")
                
                st.caption(f"Jumlah Chapter : {manga["chapters"] or rand.randint(1, 100)}")
                
                st.caption(", ".join(manga["genres"]))
                
                waktu = datetime.now(ZoneInfo("Asia/Jakarta")).isoformat()
                
                if judul in data_manhwa:
                    st.button("Tersimpan", disabled=True, use_container_width=True, key=f"tersimpan_{manga["id"]}")
                
                else:
                    if st.button("Bookmark", key=f"library_{manga["id"]}", use_container_width=True):
                        tambah = {
                            "id_user": id_user,
                            "judul_manhwa" : judul,
                            "jumlah_chapter" : manga["chapters"],
                            "genre" : ", ".join(manga["genres"]),
                            "chapter_terakhir" : None,
                            "status" : "Belum Dibaca",
                            "waktu_ditambahkan" : waktu,
                            "cover" : cover
                        }
                        
                        tambah_manhwa = (supabase.table("bookmark_user").insert(tambah)).execute()
                        
                        if len(tambah_manhwa.data) == 0:
                            st.warning("Gagal menambahkan manhwa")
                        else:
                            st.rerun()
                            st.session_state.hasil = []
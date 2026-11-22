import streamlit as st 
from database import supabase

user = st.session_state.user
st.header(f"Beranda - Koleksi {user}")

filter_status = st.selectbox("**Filter Status**", options=["Semua", "Ongoing", "Belum Dibaca"])

sort_by = st.selectbox("**Sort By**", options=["A-Z", "Z-A", "Terbaru", "Terlama"])

data_user = (supabase.table("User").select("id_user").eq("username", user).execute())
id_user = data_user.data[0]["id_user"]

data_manhwa = supabase.table("bookmark_user").select("*").eq("id_user", id_user).execute()
data = []
for i in data_manhwa.data:
    data.append(i)

def sort_manhwa(temp):
    if len(temp) <= 1:
        return temp
    
    pivot = temp[-1]
    left = []
    right = []
    
    if sort_by == "A-Z":
        for i in temp[:-1]:
            if i["judul_manhwa"].lower() < pivot["judul_manhwa"].lower():
                left.append(i)
            else:
                right.append(i)
    elif sort_by == "Z-A":
        for i in temp[:-1]:
            if i["judul_manhwa"].lower() < pivot["judul_manhwa"].lower():
                right.append(i)
            else:
                left.append(i)
    elif sort_by == "Terlama":
        for i in temp[:-1]:
            if i["waktu_ditambahkan"] < pivot["waktu_ditambahkan"]:
                left.append(i)
            else:
                right.append(i)
    elif sort_by == "Terbaru":
        for i in temp[:-1]:
            if i["waktu_ditambahkan"] < pivot["waktu_ditambahkan"]:
                right.append(i)
            else:
                left.append(i)
                
    return sort_manhwa(left) + [pivot] + sort_manhwa(right)
    
urut = sort_manhwa(data)
if "edit_manhwa" not in st.session_state:
    st.session_state.edit_manhwa = {}


st.divider()
count = 0

if filter_status == "Semua":
    cols = st.columns(3)
    for index, hasil in enumerate(urut):
        with cols[count % 3]:
            with st.container(border=True):
                cover = hasil["cover"]
                judul = hasil["judul_manhwa"]
                genre = hasil["genre"]
                status = hasil["status"]
                chapter = hasil["chapter_terakhir"]
                
                st.image(cover)
                st.write(f"**{judul}**")
                st.caption(genre)
                st.caption(f"Status: {status}")
                if status == "Ongoing":
                    st.caption(f"Chapter Terakhir: {chapter}")
                
                cols1, cols2= st.columns([1, 1], gap="xxsmall")
                with cols1:
                    if st.button("Edit Status", width="content", key=f"status_{judul}"):
                        st.session_state.edit = True
                        st.session_state.edit_manhwa = hasil
                        st.rerun()
                
                with cols2:
                    if st.button("Hapus", width="stretch" , key=f"hapus_{judul}", type="primary"):
                        hapus = (supabase.table("bookmark_user").delete().eq("id_manhwa", hasil["id_manhwa"]).execute())
                        
                        if hapus:
                            st.rerun()
                        else:
                            st.error("Gagal Hapus Bookmark!")
        count += 1

else:
    cols = st.columns(3)
    for index, hasil in enumerate(urut):
        status = hasil["status"]
        if status == filter_status:
            with cols[count % 3]:
                with st.container(border=True):
                    cover = hasil["cover"]
                    genre = hasil["genre"]
                    judul = hasil["judul_manhwa"]
                    chapter = hasil["chapter_terakhir"]
                    
                    st.image(cover)
                    st.write(f"**{judul}**")
                    st.caption(genre)
                    st.caption(f"Status: {status}")
                    if status == "Ongoing":
                        st.caption(f"Chapter Terakhir: {chapter}")
                    
                    cols1, cols2= st.columns([1, 1], gap="xxsmall")
                    with cols1:
                        if st.button("Edit Status", width="content", key=f"status_{judul}"):
                            st.session_state.edit = True
                            st.session_state.edit_manhwa = hasil
                            st.rerun()                    
                    with cols2:
                        if st.button("Hapus", width="stretch" , key=f"hapus_{judul}", type="primary"):
                            hapus = (supabase.table("bookmark_user").delete().eq("id_manhwa", hasil["id_manhwa"]).execute())
                            
                            if hapus:
                                st.rerun()
                            else:
                                st.error("Gagal Hapus Bookmark!") 
            count += 1
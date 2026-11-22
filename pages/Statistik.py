import streamlit as st 

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    with st.container(border=True):
        st.caption('Total Bookmark')
        st.header("X")
        
with col2:
    with st.container(border=True):
        st.caption("Selesai Dibaca")
        st.header("X")

with col3:
    with st.container(border=True):
        st.caption("Total Chapter Dibaca")
        st.header("X")
        
col1, col2 = st.columns([1, 1])

with col1:
    with st.container(border=True):
        st.write("**Jumlah Per Status**")
        
with col2:
    with st.container(border=True):
        st.write("**Proporsi Genre**")
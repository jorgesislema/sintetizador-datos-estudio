"""Domain selector component stub."""
import streamlit as st

def render(domains: list[str]):
    st.subheader("1. Selecciona Dominio")
    return st.selectbox("Dominio", options=domains)

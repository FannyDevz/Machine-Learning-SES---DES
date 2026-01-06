import matplotlib.pyplot as plt
import streamlit as st

def line_chart(series, title):
    fig, ax = plt.subplots()
    series.plot(ax=ax)
    ax.set_title(title)
    st.pyplot(fig)

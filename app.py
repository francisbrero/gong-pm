import streamlit as st
__import__('pysqlite3')
import sys

sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

st.set_page_config(
    page_title="Gong Calls",
    page_icon="📞",
    layout="wide",
)

with st.sidebar:
    st.markdown("# Howdy fellow human 🤠")

    st.markdown(
        """
        Instructions: 
        1. Query calls
        2. Ask Gong questions to better your knowledge of our customers
        3. Enter `can you write me a follow up email for this conversation?`
        4. If you think we're missing calls, go to Load Calls
        5. Profit 🤑
    """)

    st.divider()

    st.markdown("Made with ❤️ by the people at [MadKudu](https://madkudu.com)")


    with st.expander('Source'):
        source = """
        [Github Repo](https://github.com/francisbrero/gong-pm)
        """
        st.markdown(source, unsafe_allow_html=True)

    disclaimer = '<p style="font-size: 10px;">This LLM can make mistakes. Consider checking important information.</p>'
    st.markdown(disclaimer, unsafe_allow_html=True)
    
    page = st.sidebar.radio("Go to", ["Query Calls", "Load Calls"])
    if page == "Query Calls":
        import pages.query_calls
    elif page == "Load Calls":
        import pages.load_calls
import lorem
import streamlit as st

from streamlit_text_label import tooltip_select


@st.cache
def get_body():
    return lorem.paragraph()


def main():
    st.title("Component Gallery")
    st.header("Label selected text")
    selected = tooltip_select(get_body(), ["Noun", "Verb"])
    st.write(selected)


if __name__ == "__main__":
    main()

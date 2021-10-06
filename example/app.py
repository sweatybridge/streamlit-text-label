from random import randrange
from typing import List

import lorem
import streamlit as st

from streamlit_text_label import Selection, label_select


@st.cache
def get_body():
    return lorem.paragraph()


@st.cache
def get_labels():
    return ["Noun", "Verb"]


@st.cache
def get_selections(count: int = 5) -> List[Selection]:
    body = get_body()
    labels = get_labels()
    selected = []
    for n in range(count):
        i = randrange(len(body))
        start = i
        while start > 0 and not body[start].isspace():
            start -= 1
        end = i
        while end < len(body) and not body[end].isspace():
            end += 1
        text = body[start:end]
        label = labels[n % len(labels)]
        selected.append(Selection(start=start, end=end, text=text, labels=[label]))
    return selected


def main():
    st.title("Component Gallery")
    st.header("Label selected text")
    st.markdown(
        """
        To add a new annotation

        1. Pick a label
        2. Highlight text with cursor

        To delete an annotation

        1. Click highlighted text
        2. Press backspace

        Finally, click `Update` to propagate changes to streamlit.
        """
    )
    selected = label_select(
        body=get_body(),
        labels=get_labels(),
        selections=get_selections(),
    )
    st.write(selected)


if __name__ == "__main__":
    main()

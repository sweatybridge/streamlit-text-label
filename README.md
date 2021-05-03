# streamlit-text-label

Custom streamlit component for labelling text selections.
[screenshot](assets/screenshot.png)

## Usage

Prerequisite:

- python >= 3.6, <= 3.8

```python
from streamlit_text_label import tooltip_select

selected_text, selected_label = tooltip_select(body="lorem ipsum", labels=["Noun", "Verb"])
```

## Develop

```bash
docker-compose up
```

## Publish

```bash
cd component/frontend
npm run build
RELEASE=PROD python setup.py sdist bdist_wheel
```

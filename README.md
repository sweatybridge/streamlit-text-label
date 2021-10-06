# streamlit-text-label

Custom streamlit component for labelling text selections, based on [Label Studio](https://github.com/heartexlabs/label-studio-frontend).
![Demo](https://user-images.githubusercontent.com/1639722/136137713-752622a5-25f0-42b2-9645-a800674bff31.gif)

## Usage

Prerequisite:

- python >= 3.7

```python
from streamlit_text_label import label_select

selections = label_select(body="lorem ipsum", labels=["Noun", "Verb"])
```

More details in [example](example/app.py) directory.

## Develop

```bash
docker-compose up --build
```

Or manually, start the frontend

```bash
cd streamlit_text_label/frontend
npm install
npm run start
```

Followed by the example app

```bash
pip install -r example/requirements.txt
RELEASE=DEV streamlit run example/app.py
```

## Publish

```bash
cd component/frontend
npm run build
cd ../..
python setup.py sdist bdist_wheel
```

## Known Issues

- [ ] Labelling standalone whitespaces will not work.
- [ ] Trailing and leading whitespace will be included in selection but not rendered.
- [ ] Label colors are generated from the first 6 characters of its own MD5 hash, which may clash and have low contrast (native HSL doesn't work fully with LS).
- [ ] Each selection renders best with 1 label only. If you need multiple labels, create multiple selections.

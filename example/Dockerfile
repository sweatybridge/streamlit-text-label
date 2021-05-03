FROM python:3.8

WORKDIR /app

COPY setup.py .
COPY streamlit_text_label/__init__.py ./streamlit_text_label/
COPY example/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["streamlit", "run", "app.py"]

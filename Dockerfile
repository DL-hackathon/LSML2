FROM python:3.10
LABEL authors="Dmitry_Lazarev"
WORKDIR /code
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY main.py .
COPY ./static static
COPY ./templates templates
EXPOSE 80/tcp
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
FROM python:3.10

RUN apt-get update && apt-get install -y \
    firefox-esr \
    wget \
    unzip \
    && apt-get clean


RUN GECKODRIVER_VERSION=v0.30.0 \
    && wget https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VERSION}/geckodriver-${GECKODRIVER_VERSION}-linux64.tar.gz \
    && tar -xvzf geckodriver-${GECKODRIVER_VERSION}-linux64.tar.gz \
    && mv geckodriver /usr/local/bin/ \
    && rm geckodriver-${GECKODRIVER_VERSION}-linux64.tar.gz

WORKDIR /app

COPY requirements.txt .


RUN mkdir -p /app/output_folder && chmod -R 777 /app/output_folder
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install uvicorn

COPY . .

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
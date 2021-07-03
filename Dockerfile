FROM python:3.9.2
WORKDIR /app
COPY . .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
ENV FLASK_APP app.py
ENV FLASK_ENV=development
EXPOSE 5000
CMD ["python", "-m", "flask", "run" , "--host", "0.0.0.0"]
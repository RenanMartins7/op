FROM python:3.10-slim

WORKDIR /app
COPY ia.py .
COPY scrap.py .


RUN pip install requests \
numpy \
pandas \
scikit-learn \
joblib

CMD ["bash"]
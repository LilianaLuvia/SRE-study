FROM python:3.13-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /SRE-STUDY
COPY . .
RUN pip install psutil
RUN pip install pymysql
CMD ["python", "main_sre_engine.py"]
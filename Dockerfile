
# Pull official base Python Docker image
FROM python:3.10.6
#set workdir
WORKDIR /usr/src/app
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Install dependencie
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY ./wait-for-it.sh .
RUN chmod +x /usr/src/app/wait-for-it.sh
# Copy the Django project
COPY . .
ENTRYPOINT ["bash","/usr/src/app/wait-for-it.sh"]





#### Set base image (host OS)
FROM python:3.12-alpine

#### By default, listen on port 5000
EXPOSE 5000/tcp

#### Set the working directory in the container
WORKDIR /

#### Copy the dependencies file to the working directory
COPY requirements.txt .

#### Install any dependencies
RUN pip install -r requirements.txt

#### Copy the content of the local src directory to the working directory
COPY . .

#### Specify the command to run on container start
# CMD [ "python", "run.py" ]
CMD ["waitress-serve", "--host", "0.0.0.0", "--port", "8080", "app:application"]
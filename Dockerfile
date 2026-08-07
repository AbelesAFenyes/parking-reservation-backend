# 1. Grab a lightweight version of Python
FROM python:3.10-slim

# 2. Create a folder inside the container named /code
WORKDIR /code

# 3. Copy our shopping list into the container and install everything
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r /code/requirements.txt

# 4. Copy all our beautiful Python files into the container
COPY ./app /code/app

# 5. Tell the container how to turn on the Uvicorn server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
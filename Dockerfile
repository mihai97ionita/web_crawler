FROM mihai97ionita/web-crawler:python_crawler_base

#venv
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies:
COPY requirements.txt .
RUN pip install -r requirements.txt

# Run the application:
WORKDIR app
COPY . .
EXPOSE 1007
CMD ["python", "main.py"]

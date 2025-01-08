@echo off

:: Build the Docker image
docker build -t zkraper:V0 .

:: Run the Docker container
docker run -it -v "%cd%":/app --rm zkraper:V0 python -m main --base-url "https://www.marca.com" --max-scrapers 10

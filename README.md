# autoria-scrapping
1. Install Docker Desktop
2. In cmd: Install WSL: wsl --install or Update WSL: wsl --update
2. pull repository in local folder: git pull repo_link
3. build docker: docker build -t aurtoria:latest .
4. docker-compose up --build
In order to stop:
1. docker-compose down -v
2. docker volume rm postgres_data

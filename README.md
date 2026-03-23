# mini_htmx_app
A tiny Flask based web app using HTMX

This app is meant to be a small single pane app using HTMX to implement the UI.
It supports a very simple database of people contacts. The goal is a minimal functional application to explore using HTMX.

## Run Locally

### Setup

Create a virtual environment and install the required libraries.

If you are using the tool uv:
```
uv venv
uv pip install -r requirements.txt
```

If you are using pip:
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
deactivate
```

### Populate the database 
Add entries with fake data by running:
```
source .venv/bin/activate
python pop_db.py 20
deactivate
```
### Run the application
```
source .venv/bin/activate
python main.py
deactivate
```

Open [http://localhost:8080](http://localhost:8080)


## Run with Docker

Using Docker is a great way to run apps more safely in relative isolation.

### Build Image
To build an image named contacts:
```
docker build -t contacts .
```

### Create Container
To run in a container named contacts:
```
docker create --name contacts -p 8080:8080 contacts
```

### Start
```
docker start -a contacts
```

### Populate the database 
Add entries with fake data by running:
```
docker exec -it contacts ./pop_db.py 20
```

### Stop
```
docker stop contacts
```

### Cleanup
```
docker container rm contacts
docker image rm contacts
```




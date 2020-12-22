# DevOps Apprenticeship: Project Exercise

## Getting started

Run locally via 
```bash
poetry run flask run
```

Run via Docker 
```bash
docker build --target development --tag todo-app:dev .  
docker run --env-file ./.env -p5000:5000 --mount type=bind,source="$(pwd)"todo_app,target=/app/todo_app todo-app:dev


### Running the tests in a Docker container 

To run the tests in a Docker container, run  `docker build --tag test --target test .` to build the container and
 * `docker run --env-file .env test tests/test_viewmodel.py` to run unit test
 * `docker run --env-file .env test tests/test_integration.py` to run integration test
 * `docker run --env-file .env test test tests/test_e2e.py` to run end-to-end test
 
  
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

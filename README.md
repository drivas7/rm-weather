<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="https://i.imgur.com/6wj0hh6.jpg" alt="Project logo"></a>
</p>

<h3 align="center">RM WeatherApp</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()

</div>

---

<p align="center"> A simple Weather App.
    <br> 
</p>

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Running the Tests](#tests)
- [Endpoints](#endpoints)
- [Running the App](#running)
- [Deploying the App](#deploying)


## 🧐 About <a name = "about"></a>

The prompt that started this project was the following: 

```
Create a small Python application following state-of-the-art standards and best practices in terms of craftsmanship.

Using FastAPI, expose these endpoints:

/temperature: what will be the temperature in Lisbon in 3 days?
/rain: Will it rain in Lisbon in 3 days?
This should be reflecting real data, fetched from any API of your choice.

Ensure the application is unit tested correctly and is overall built to be highly maintainable. A README is a must.
```


## 🏁 Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 


### Installing

The steps to install the project are the following:

1. Ensure python3 is installed, as well as pip.

2. Install all requirements by running the following command on the root folder of the repository.

```bash
pip install -r requirements.txt
```

3. Set up the environment variables: WEATHER_API_URL, TEMPERATURE_PARAMS, RAIN_PARAMS

| Variable           | Description                                                  |
| ------------------ | ------------------------------------------------------------ |
| `WEATHER_API_URL`  | URL of the weather API. Ensure that this environment variable is set to the appropriate URL. |
| `TEMPERATURE_PARAMS`  | List of parameters passed to the URL of the weather API when querying the temperature endpoint. |
| `RAIN_PARAMS`  | List of parameters passed to the URL of the weather API when querying the rain endpoint. |
| `GEOLOCATION_API_URL`  | URL of the geolocation API. Ensure that this environment variable is set to the appropriate URL. |


```bash
export WEATHER_API_URL = {value} 
export TEMPERATURE_PARAMS = {value}
export RAIN_PARAMS = {value}
export GEOLOCATION_API_URL = {value}
```

## 🔧 Running the Tests <a name = "tests"></a>

The tests for this project verify that the response is 200, that it has all expected parameters, and the performance.

### How to Test

1. Set up the temporary env variable PYTHONPATH 

```bash
export PYTHONPATH = path/to/project
```
2. Run the tests.
```bash
pytest
```

## 🎈 Endpoints <a name="endpoints"></a>

The usage of the system is pretty simple. The weather app has two different endpoints:

- `/temperature`: This endpoint retrieves the temperature forecast for a specified city. It returns the forecast for the next 3 days, including the maximum and minimum temperatures, apparent temperatures, sunrise and sunset times, and a description of the weather conditions.
  - It can optionally receive the `?city=` parameter in the URL. In this case, the city's name needs to be in English. The default value is Lisbon. 
  - It can optionally receive the `?days=` parameter in the URL. It cannot be greater than 16, and the default value is 0, which returns the weather of 3 days from now.
- `/rain`: This endpoint checks if it will rain in a specified city in the next 3 days. It returns information about rainfall, including the sum of rain and showers, precipitation probability, and maximum wind speed.
  - It can optionally receive the `?city=` parameter in the URL. In this case, the city's name needs to be in English. The default value is Lisbon.
  - It can optionally receive the `?days=` parameter in the URL. It cannot be greater than 16, and the default value is 0, which returns the weather of 3 days from now.


## 🚀 Running the App <a name = "running"></a>

Running the app only requires executing the following command from the root of the project:

```bash
python main.py
```

Alternatively, it can run using the Dockerfile:

```bash
docker build -t rm-weather --build-arg WEATHER_API_URL=$WEATHER_API_URL --build-arg TEMPERATURE_PARAMS=$TEMPERATURE_PARAMS --build-arg RAIN_PARAMS=$RAIN_PARAMS --build-arg GEOLOCATION_API_URL=$GEOLOCATION_API_URL .

docker run -p 8000:8000 rm-weather
```

## 🚀🚀 Deploying the App (CI/CD Overview) <a name = "deploying"></a>


This CI/CD pipeline automates the testing and deployment process for the project on GitHub. It consists of two main jobs: `build` and `deploy`.

### Build Job

- **Trigger**: This job is triggered on every push to the `main` branch.
- **Environment**: It runs on an Ubuntu environment (`ubuntu-latest`).
- **Steps**:
  - Checks out the code repository using `actions/checkout`.
  - Sets up a Python environment with the specified version using `actions/setup-python`.
  - Installs project dependencies defined in `requirements.txt`.
  - Runs tests using pytest to ensure code quality and functionality.

### Deploy Job

- **Trigger**: This job runs after the `build` job and depends on its successful completion (`needs: build`).
- **Environment**: It also runs on an Ubuntu environment.
- **Steps**:
  - Copies project files to an AWS EC2 instance for deployment using the `appleboy/scp-action` GitHub Action.
  - Passes environment variables (`WEATHER_API_URL`, `TEMPERATURE_PARAMS`, and `RAIN_PARAMS`, `GEOLOCATION_API_URL`) required for the application to the Docker container during deployment using GitHub Secrets.
  - The Docker container runs the FastAPI application using uvicorn, exposing it on port 8000.

### Tests (pytest)

- Pytest is used to automate the testing process in the `build` job.
- It verifies code quality and functionality by executing unit tests defined in the project.
- Test results are crucial for ensuring that the application behaves as expected and meets the specified requirements.


### GitHub Secrets

- GitHub Secrets are used to securely store sensitive information such as API keys, passwords, and tokens.
- Environment variables required for the application (`WEATHER_API_URL`, `TEMPERATURE_PARAMS`, `GEOLOCATION_API_URL` and `RAIN_PARAMS`) are stored as GitHub Secrets and accessed in the workflow YAML file using `${{ secrets.SECRET_NAME }}` syntax.

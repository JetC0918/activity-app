# Activity Planner Assistant

## Problem Description

Planning and organizing activities can be a daunting and time-consuming task for many people, whether it involves finding fun family activities, selecting engaging indoor projects for children, or planning group events. The process often involves manually searching through multiple sources to find relevant activities that match specific needs, such as age group, difficulty level, or time constraints.

The **Activity Planner Assistant** addresses these problems by providing an intelligent and interactive solution to help users efficiently find, replace, and understand activities tailored to their needs.

## What The Application Do

The **Activity Planner Assistant** is an intelligent tool designed to simplify the process of planning and organizing activities. By leveraging advanced retrieval techniques, this application helps users quickly find, customize, and execute a wide range of activities suited to their preferences and needs. The assistant supports the following functions:

1. **Discover Activities:** Users can explore a diverse range of activities based on various filters, such as age group, activity type (indoor or outdoor), time required, and difficulty level.
2. **Personalize Recommendations:** The assistant offers personalized suggestions for new activities or alternatives to existing plans, taking into account user preferences and constraints.
3. **Access Step-by-Step Guidance:** For each selected activity, users can obtain detailed, step-by-step instructions along with a list of required materials, ensuring a smooth and hassle-free experience.
4. **Optimize Activity Planning:** Users can receive suggestions on how to adapt activities to different scenarios, such as limited resources or varying group sizes. 

By using the **Activity Planner Assistant**, users can save time, reduce effort, and make more informed decisions when planning activities, ensuring a more enjoyable and stress-free experience.

## Dataset

The dataset used in this project, generated with the help of ChatGPT, contains 240 records and is located in the `data` folder. Each record provides detailed information about a variety of activities, including:

- **id**: A unique identifier for each activity.
- **activity_name**: The name of the activity (e.g., "Family Picnic", "DIY Craft Project").
- **activity_type**: The type of activity (e.g., Indoor, Outdoor).
- **materials_needed**: A list of materials required to perform the activity.
- **time_required**: The estimated time to complete the activity.
- **age_group**: The suitable age group for the activity (e.g., Toddlers, School-aged).
- **difficulty_level**: The difficulty level of the activity (e.g., Easy, Moderate, Challenging).
- **instructions**: Step-by-step instructions on how to perform the activity.

Dataset can be found in  [data/data.csv](data/data.csv)

## Technologies

* Python 3.12
* Docker and Docker Compose for containerization
* [Minsearch](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/01-intro/minsearch.py) - for 
full-text search
* OpenAI as LLM
* Grafana for monitoring and PostgreSQL as the backend for it
* Flask as the API interface (see [Background](#background)
for more infomation on Flask)

## Preparation 

We are using OpenAI so we need to provide the API key:

1. Install `direnv`.
2. Copy `.envrc_template` into `.envrc` and insert your key there.
3. For OpenAI, it's recommended to create a new project and use a separate key.
4. Run direnv allow to load the key into your environment.

For dependency management, we use pipenv, so you need to install it:

```bash

pip install pipenv

```

Once installed, you can install the app dependencies:

```bash

pipenv install --dev

```

## Running the application
### Database configuration

Before the application starts for the first time, the database needs to be initialized.

First, run postgres:
```bash
docker-compose up postgres
```
Then run the `db_prep.py` script:

```bash
pipenv shell

cd fitness_assistant

export POSTGRES_HOST=localhost
python db_prep.py
``` 

### Running with Docker-Compose
The easiest way to run the application is with docker-compose:

``` bash
docker-compose up
```

### Running locally 
### Installing the dependencies:

If you want to run the application locally, start only postres and grafana:

``` bash

docker-compose up postgres grafana

```
If you previously started all applications with docker-compose up, you need to stop the app:

``` bash

docker-compose stop app

```  
Now run the app on your host machine:
 
```bash
pipenv shell

cd fitness_assistant

export POSTGRES_HOST=localhost
python app.py
``` 

## Using the application
When the application is running, we can start using it.

### CLI
We built an interactive CLI application using [questionary](https://questionary.readthedocs.io/en/stable/).

To start it, run:

``` bash
pipenv run python cli.py
```

You can also make it randomly select a question from our ground truth dataset:

``` bash
pipenv run python cli.py --random
```

### Using requests
When the application is running, you can use requests to send questions—use test.py for testing it:

``` bash
pipenv run python test.py
``` 

It will pick a random question from the ground truth dataset and send it to the app.

### CURL
You can also use `curl` for interacting with the API:

```bash  

URL=http://localhost:5000
QUESTION="What materials do I need for the Family Picnic?"
DATA='{
    "question": "'${QUESTION}'"
}'

curl -X POST \
    -H "Content-Type: application/json" \
    -d "${DATA}" \
    ${URL}/question
```

You will see the following response:
```bash
  "answer": "For the Family Picnic, you will need the following materials: a picnic blanket, a basket of food, and drinks.",
  "conversation_id": "0b21d0f3-c6df-492e-b2b3-fdf455552924,
  "question": "What materials do I need for the Family Picnic?"
```

Sending feedback:
```bash
ID="0b21d0f3-c6df-492e-b2b3-fdf455552924"

URL=http://localhost:5000
FEEDBACK_DATA='{
    "conversation_id": "'${ID}'",
    "feedback": 1
}'

curl -X POST \
    -H "Content-Type: application/json" \
    -d "${FEEDBACK_DATA}" \
    ${URL}/feedback
```

After sending, you will receive the acknowledgement:
```bash
{
  "message": "Feedback received for conversation 0b21d0f3-c6df-492e-b2b3-fdf455552924: 1" 
}
```

Alternatively, you can use [test.py](activity-app/test.py) for testing it:

```bash
pipenv run python test.py
```

## Code
The code for the application is in the `activity_planner` folder:

* [app.py](activity-app/app.py)- the Flask API, the main entrypoint to the application
* [rag.py](activity-app/rag.py) - the main RAG logic for building the retrieving the data and building the prompt
* [ingest.py](activity-app/ingest.py) - loading the data into the knowledge base
* [minsearch.py](activity-app/minsearch.py) - an in-memory search engine
* [db.py](activity-app/db.py) - the logic for logging the requests and responses to postgres
* [db_prep.py](activity-app/db_prep.py) - the script for initializing the database
We also have some code in the project root directory:

* [test.py](test.py) - select a random question for testing
* [cli.py](cli.py) - interactive CLI for the APP

## Interface

We use Flask for serving the application as API.

Refer to [Running The Application](#running-the-application)
section for details

## Ingestion
The ingestion script is in [activity-app/ingest.py]
(activity-app/ingest.py) and it's run on the startup
of the app (in [activity-app/rag.py]
(activity-app/rag.py) )
 
## Evaluation

For the code evaluation system, you can check 
the [notebooks/rag-test.ipynb](notebooks/rag-test.ipynb)
notebook.

### Retrieval
The basic approach - using minsearch without any boosting
- gave the following metrics

* Hit Rate: 89%
* MRR: 82%

The improved version (with better boosting):

* Hit Rate: 89%
* MRR: 83%

The best boosting parameters:
```python
{
      'activity_name': 3.94,
      'activity_type': 3.99,
      'materials_needed': 1.14,
      'time_required': 0.73,
      'age_group': 1.05,
      'difficulty_level': 1.86,
      'instructions': 2.00
        }
```

### RAG Flow
We used the LLM-as-a-Judge metric to evaluate the quality
of our RAG flow.

For gpt-4o-mini, among 200 records, we had:

* 153(76%) RELEVANT
* 46(23%) PARTLY_RELEVANT
* 1(0.5%) IRRELEVANT

For gpt-4o, among 200 records, we had:

* 158(79%) RELEVANT
* 41(20%) PARTLY_RELEVANT
* 1(0.5%) IRRELEVANT

The difference is not very significant, so we proceed with gpt-4o-mini

## Monitoring
We use Grafana for monitoring the application.

It's accessible at (localhost:3000)[localhost:3000]:

Login: "admin"
Password: "admin"

### Dashboards
[dashboard](image/image.png)
The monitoring dashboard contains several panels:

1. **Last 5 Conversations (Table)**: Displays a table showing the five most recent conversations, including details such as the question, answer, relevance, and timestamp. This panel helps monitor recent interactions with users.
2. **+1/-1 (Pie Chart)**: A pie chart that visualizes the feedback from users, showing the count of positive (thumbs up) and negative (thumbs down) feedback received. This panel helps track user satisfaction.
3. **Relevancy (Gauge)**: A gauge chart representing the relevance of the responses provided during conversations. The chart categorizes relevance and indicates thresholds using different colors to highlight varying levels of response quality. 

### Starting Grafana
All Grafana configurations are in the (grafana)[grafana/] folder:

* (init.py)[grafana/init.py] - for initializing the datasource and the dashboard.
* (dashboard.json)[grafana/dashboard.json] - the actual dashboard (taken from LLM Zoomcamp without changes).
To initialize the dashboard, first ensure Grafana is running (it starts automatically when you do docker-compose up).

Then run:

``` bash
pipenv shell

cd grafana

# make sure the POSTGRES_HOST variable is not overwritten 
env | grep POSTGRES_HOST

python init.py
```

Then go to (localhost:3000)[localhost:3000]:

* Login: "admin"
* Password: "admin"
When prompted, keep "admin" as the new password.

## Background
Here we provide background on some tech not used in the course and links for further reading.

### Flask   
We use Flask for creating the API interface for our application. It's a web application framework for Python: we can easily create an endpoint for asking questions and use web clients (like `curl` or `requests`) for communicating with it.

In our case, we can send questions to `http://localhost:5000/question`.

For more information, visit the [official Flask documentation](https://flask.palletsprojects.com/).

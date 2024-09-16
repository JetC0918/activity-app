# Activity Planner Assistant

## Problem Description

Planning and organizing activities can be a daunting and time-consuming task for many people, whether it involves finding fun family activities, selecting engaging indoor projects for children, or planning group events. The process often involves manually searching through multiple sources to find relevant activities that match specific needs, such as age group, difficulty level, or time constraints.

The lack of a centralized, easy-to-use tool for activity planning leads to several problems:
- **Inefficient Activity Selection:** Users spend a significant amount of time searching for suitable activities, often without finding something that meets their needs.
- **Limited Customization:** It's challenging to tailor activities to specific requirements, such as available materials, age appropriateness, or preferred difficulty level.
- **Lack of Detailed Guidance:** Even when an activity is chosen, users may struggle to find clear instructions or necessary materials to execute the activity successfully.

The **Activity Planner Assistant** addresses these problems by providing an intelligent and interactive solution to help users efficiently find, replace, and understand activities tailored to their needs.

## What The Application Do

The **Activity Planner Assistant** is an intelligent tool designed to simplify the process of planning and organizing activities. By leveraging advanced retrieval techniques, this application helps users quickly find, customize, and execute a wide range of activities suited to their preferences and needs. The assistant supports the following functions:

1. **Discover Activities:** Users can explore a diverse range of activities based on various filters, such as age group, activity type (indoor or outdoor), time required, and difficulty level.
2. **Personalize Recommendations:** The assistant offers personalized suggestions for new activities or alternatives to existing plans, taking into account user preferences and constraints.
3. **Access Step-by-Step Guidance:** For each selected activity, users can obtain detailed, step-by-step instructions along with a list of required materials, ensuring a smooth and hassle-free experience.
4. **Optimize Activity Planning:** Users can receive suggestions on how to adapt activities to different scenarios, such as limited resources or varying group sizes. 

### Key Features

- **Interactive Chat:** Users can interact with the assistant in natural language to receive personalized suggestions and guidance.
- **Quick Access to Activity Information:** Retrieve detailed activity information from a curated dataset, saving time and effort.
- **Customizable and Adaptive Planning:** Tailor activity planning to specific needs, making the experience flexible and user-friendly.

By using the **Activity Planner Assistant**, users can save time, reduce effort, and make more informed decisions when planning activities, ensuring a more enjoyable and stress-free experience.


## Technologies

* [Minsearch](https://github.com/DataTalksClub/llm-zoomcamp/blob/main/01-intro/minsearch.py) - for 
full-text search
* OpenAI as LLM
* Flask as the API interface (see [Background](#background)
for more infomation on Flask)

## Data

The dataset used in this project, generated with the help of ChatGPT, contains 240 records and is located in the `data` folder. Each record provides detailed information about a variety of activities, including:

- **id**: A unique identifier for each activity.
- **activity_name**: The name of the activity (e.g., "Family Picnic", "DIY Craft Project").
- **activity_type**: The type of activity (e.g., Indoor, Outdoor).
- **materials_needed**: A list of materials required to perform the activity.
- **time_required**: The estimated time to complete the activity.
- **age_group**: The suitable age group for the activity (e.g., Toddlers, School-aged).
- **difficulty_level**: The difficulty level of the activity (e.g., Easy, Moderate, Challenging).
- **instructions**: Step-by-step instructions on how to perform the activity.

Here is an example of the data:

| activity_name      | activity_type | materials_needed                     | time_required | age_group   | difficulty_level | instructions                                                                                                 |
|--------------------|---------------|--------------------------------------|---------------|-------------|------------------|--------------------------------------------------------------------------------------------------------------|
| Family Picnic      | Outdoor       | Picnic blanket, Basket of food, Drinks | 2 hours       | Toddlers    | Easy             | Spread out the blanket, arrange the food and drinks, and enjoy a meal together in a park or backyard.        |
| DIY Craft Project  | Indoor        | Craft supplies, Glue, Scissors         | 1 hour        | School-aged | Moderate         | Choose a craft project, gather all necessary supplies, and follow the steps to complete the craft. Supervise children with glue and scissors. |
| Board Game Night   | Indoor        | Board games, Snacks                    | 2 hours       | Teens       | Easy             | Select a few board games, set up a comfortable area for playing, and enjoy a night of games and snacks with family or friends. |


## Running it with Docker 
The easiest way to run this application is with Docker
```bash
docker-compose up
```

If you need to change something in the dockerfile and test
it quickly, you can use the following command:

```bash 
docker build -t activity-app .

docker run -it --rm \
    -e OPENAI_API_KEY=${OPENAI_API_KEY} \
    -e DATA_PATH="data/data.csv" \
    -p 5000:5000 \
    activity-app 
```

## Running locally 
### Installing the dependencies:

If you dont use Docker and want to run locally,
you need to manually install the environment and install
all the dependencies.

We use pipenv for managing dependencies and Python 3.12.

Make sure you have `pipenv` installed

```bash
pip install pipenv
```

Installing the dependencies:

```bash
pipenv install --dev
```

## Prepare the application 

Before we can use the app, we need to initialize the database.

We can do it by running [`db_prep.py`](activity-app/db_prep.py) script:

```bash
cd activity-app

pipenv shell

export POSTGRES_HOST=localhost 
python db_prep.py
```

## Running the application:

For runnnig the application locally, do this:

Running the Flask application:
```bash 
pipenv shell

export POSTGRES_HOST=localhost  
python app.py
```

## Using the application

First, you need to run the application either with
docker-compose or locally.

When it's running, let's test it:
 
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

The response will be something like this:
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

## Background
Here we provide background on some tech not used in the course and links for further reading.

### Flask   
We use Flask for creating the API interface for our application. It's a web application framework for Python: we can easily create an endpoint for asking questions and use web clients (like `curl` or `requests`) for communicating with it.

In our case, we can send questions to `http://localhost:5000/question`.

For more information, visit the [official Flask documentation](https://flask.palletsprojects.com/).
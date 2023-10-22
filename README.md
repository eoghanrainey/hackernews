# Async HackerNews API Reader

A FastAPI based application that asynchronously reads data from the HackerNews API and exposes it through a set of RESTful endpoints.

## Table of Contents
1. [Problem Statement](#problem-statement)
2. [Installation and Usage](#installation-and-usage)
3. [Usage with Docker](#usage-with-docker)
4. [API Endpoints](#api-endpoints)
5. [Scaling and Performance](#scaling-and-performance)
6. [Automated Testing](#automated-testing)
7. [Continuous Integration/Continuous Deployment (CI/CD)](#continuous-integrationcontinuous-deployment-cicd)
8. [Future Improvements](#future-improvements)

## Problem Statement

The application is designed to solve the following challenges:

1. Return the first 50 comments made to the first 100 top stories at any given moment.
2. Return the 10 most used words for the first 100 comments for the top 30 stories.
3. Return the most used words in all comments, including nested comments, of the first 10 stories.

## Installation and Usage

Clone the repository and install the dependencies:

```bash
git clone https://github.com/eoghanrainey/hackernews
pip install -r requirements.txt
```

Run the application:

```bash
uvicorn main:app --reload
```

## Usage with Docker

If you have [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) installed, you can use `docker-compose` to run the application in a Docker container.

```bash
docker-compose up
```

This will build the Docker image for your application and start a container. Your application will be accessible at `localhost:8000`.

To access the auto-generated Swagger UI documentation for your API, navigate to `localhost:8000/docs` in your web browser.

## API Endpoints

1. `/first_fifty_comments/`: Returns the first 50 comments (excluding nested comments) from the top 100 stories at the moment.
2. `/top_comment_words/`: Returns the 10 most used words from the first 100 comments (excluding nested comments) of the top 30 stories.
3. `/most_used_words_nested_comments/`: Returns the most used words in all comments, including nested comments, from the first 10 stories.

## Scaling and Performance

To scale the application to handle more requests per second, several strategies could be implemented:

1. **Load Balancer**: Use a load balancer to distribute incoming network traffic across multiple servers.
2. **Horizontal Scaling**: Add more machines to the network as the demand increases.
3. **Asynchronous Tasks**: Make long-running tasks asynchronous or offload them to a separate worker process.
4. **Code Optimization**: Time was limited and code is efficient, we could optimise this to not cause any unnecessary delays.
7. **Application Caching**: Implement application-level caching to store the results of expensive operations.
8. **Serverless Architecture**: Consider using a serverless architecture, such as AWS Lambda or Google Cloud Functions.

## Automated Testing

Automated testing can be done by using testing frameworks such as `pytest`. We can write unit tests for our functions and integration tests for our API endpoints. These tests can be run automatically using continuous integration tools like Jenkins or GitHub Actions whenever code is pushed to the repository.

## Continuous Integration/Continuous Deployment (CI/CD)

A CI/CD pipeline can be implemented using tools like Jenkins, Travis CI, or GitHub Actions. The pipeline would include stages for installing dependencies, running automated tests, building the application, and deploying it to a staging environment. If all stages pass, the application can then be deployed to production.

## Future Improvements

While the application is fully functional, there are areas where it can be improved:

1. **Error Handling**: Implement better error handling for scenarios where the HackerNews API might be unavailable or return error responses.
2. **Nested Comment Handling**: Improve the efficiency of handling nested comments.
3. **Enhanced Testing**: Increase the coverage of automated tests to include more edge cases.
4. **Redis** can be a significant help in scaling a web application like this one, especially in the following aspects:

Caching: As an in-memory data store that can be used as a cache. It is super fast and can reduce the load on  database(if impl) by caching the results of expensive or frequently accessed API calls. For example, you could cache the results of the HackerNews API calls, and when the same data is requested, you could return the cached data instead of making another API call.

Rate Limiting: The application could implement rate limiting to prevent abuse (which is especially important for public APIs), Redis can store the IP address and the number of requests made by each user and reset it after a certain period.


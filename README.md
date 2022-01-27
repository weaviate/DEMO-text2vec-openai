# DEMO-text2vec-openai

This repository contains an example of how to use the Weaviate [text2vec-openai module](https://www.semi.technology/developers/weaviate/current/modules/text2vec-openai.html). When using this demo dataset, Weaviate will vectorize the data _and_ the queries based on OpenAI's [Babbage](https://beta.openai.com/docs/engines/babbage) model.

#### About the Dataset

This dataset contains descriptions of 34,886 movies from around the world. The dataset is taken from [Kaggle](https://www.kaggle.com/jrobischon/wikipedia-movie-plots).

## Run the setup

Before running this setup, make sure you have an OpenAPI ready, you can create one [here](https://beta.openai.com/account/api-keys).

### 1. Run the container

Inside `docker-compose.yml` update the environment variable `APIKEY` with your OpenAI API key. After this, run the container by running:

```sh
$ docker-compose up -d
```

### 2. Import the data

After the container starts up, you can import the data by running:

```sh
# Install the Weaviate Python client
$ pip3 install -r requirements.txt
# Import the data
$ pip3 ./load.py
```

Note: because the OpenAI API comes with a rate limit, we have taken this into account for this demo dataset. If you work with your own dataset _and_ you've requested an increase/removal of your rate limit, you can increase the import speed. You can read [here](https://www.semi.technology/developers/weaviate/current/modules/text2vec-openai.html#openai-rate-limits) how to do this.

### 3. Query the data

You can query the data via the GraphQL interface that's available in the [Weaviate Console](https://console.semi.technology/) (under "Self Hosted Weaviate").

Or you can test the example queries below.

## Example Queries

```graphql
{}
```
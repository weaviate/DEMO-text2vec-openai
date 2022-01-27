# Weaviate demo with the text2vec-openai module

This repository contains an example of how to use the Weaviate [text2vec-openai module](https://www.semi.technology/developers/weaviate/current/modules/text2vec-openai.html). When using this demo dataset, Weaviate will vectorize the data _and_ the queries based on OpenAI's [Babbage](https://beta.openai.com/docs/engines/babbage) model.

## What is Weaviate?

Weaviate is an open-source, modular vector search engine. It works like any other database you're used to (it has full [CRUD support](https://db-engines.com/en/blog_post/87), it's cloud-native, etc), but it is created around the concept of storing all data objects based on the vector representations (i.e., embeddings) of these data objects. Within Weaviate you can mix traditional, scalar search filters with vector search filters through its [GraphQL-API](https://www.semi.technology/developers/weaviate/current/graphql-references/).

[Weaviate modules](https://www.semi.technology/developers/weaviate/current/configuration/modules.html) can be used to -among other things- vectorize the data objects you add to Weaviate. In this demo, the [text2vec-openai](https://www.semi.technology/developers/weaviate/current/modules/text2vec-openai.html) module is used to vectorize all data using OpenAI's Babbage model.

You can read about Weaviate in more detail in the [software docs](https://www.semi.technology/developers/weaviate/current/).

#### About the Dataset

This dataset contains descriptions of 34,886 movies from around the world. The dataset is taken from [Kaggle](https://www.kaggle.com/jrobischon/wikipedia-movie-plots).

## Run the setup

Before running this setup, make sure you have an OpenAPI ready, you can create one [here](https://beta.openai.com/account/api-keys).

### 0. Update you OpenAI API key

```
$ export OPENAI_APIKEY=YOUR_API_KEY
```

### 1. Run the container

Run the container:

```sh
$ docker-compose up -d
```

### 2. Import the data

After the container starts up, you can import the data by running:

```sh
# Install the Weaviate Python client
$ pip3 install -r requirements.txt
# Import the data with the format `./import.py {URL} {OPENAI RATE LIMIT}`
$ ./import.py http://localhost:8080 550
```

Note: because the OpenAI API comes with a rate limit, we have taken this into account for this demo dataset. If you work with your own dataset _and_ you've requested an increase/removal of your rate limit, you can increase the import speed. You can read [here](https://www.semi.technology/developers/weaviate/current/modules/text2vec-openai.html#openai-rate-limits) how to do this.

### 3. Query the data

You can query the data via the GraphQL interface that's available in the [Weaviate Console](https://console.semi.technology/) (under "Self Hosted Weaviate").

Or you can test the example queries below.

## Example Queries

```graphql
{}
```
#!/usr/bin/env python3
"""
Import data into weaviate script.
"""
import os
from posixpath import split
import sys
import json
import time
import uuid
from typing import Callable, Optional
from weaviate import Client
# from load.data import Loader

def generate_uuid(key: str) -> str:
    """
    Generate an universally unique identifier (uuid).
    Parameters
    ----------
    key : str
        The key used to generate the uuid.
    Returns
    -------
    str
        Universally unique identifier (uuid) as string.
    """

    return str(uuid.uuid3(uuid.NAMESPACE_DNS, key))

def batch_callback(results: Optional[list]) -> None:
    """
    Log error message that comes from the batcher update.
    Parameters
    ----------
    results : Optional[list]
        A list of result for object that were uploaded to Weaviate using the batcher.
    """

    if results is not None:
        for result in results:
            if 'result' in result and 'errors' in result['result']:
                if 'error' in result['result']['errors']:
                    for message in result['result']['errors']['error']:
                        print(message['message'])


def split_items(n: str, i: str):
    return i[n].replace("Director: ", "").replace("Cast: ", "").split(",")


def add_class_items(client: Client, name: str, data: dict, batch_size: int):
    c = 0
    uuid_list = []
    for movie in data:
        items = split_items(name, movie)
        for item in items:
            item = item.strip()
            if generate_uuid(item) not in uuid_list:
                client.batch.add_data_object({
                    "name": item
                }, name, generate_uuid(item))
                uuid_list.append(generate_uuid(item))
                c = c + 1
                if c == batch_size:
                    print("Add batch of", name)
                    client.batch.create_objects()
                    client.batch.empty_objects()
                    c = 0
    print("Add batch of", name)
    client.batch.create_objects()
    client.batch.empty_objects()


def upload_data_to_weaviate(client: Client, batch_size: int = 200) -> None:
    """
    Initiate upload data to weaviate.
    Parameters
    ----------
    client: weaviate.Client
        The Weaviate client.
    data_dir: str
        Directory with the data files to read in.
    batch_size:int = 200
        Number of objects to upload at once to weaviate.
    """

    client.batch.configure(
        batch_size=batch_size,
        dynamic=True,
        timeout_retries=5,
        callback=batch_callback,
    )

    f = open('data/movies.json')
    data = json.load(f)

    print("Import all movie data")

    # add the Directors, Cast, Genres
    add_class_items(client, "Director", data, batch_size)
    add_class_items(client, "Cast", data, batch_size)
    add_class_items(client, "Genre", data, batch_size)

    # add the movie
    print("Add Movies")
    c = 0
    start = time.time()
    for movie in data:
        client.batch.add_data_object({
            "year": int(movie["Release Year"]),
            "title": movie["Title"],
            "origin": movie["Origin/Ethnicity"],
            "wiki": movie["Wiki Page"],
            "plot": movie["Plot"]
        }, "Movie", generate_uuid(movie["Title"]))
        c = c + 1
        if c == batch_size:
            print("Add batch of Movies")
            client.batch.create_objects()
            client.batch.empty_objects()
            c = 0
            stop = time.time()
            print("⌛ The OpenAI rate limit is set to", batch_size, " per minute")
            print("⌛ Sleep for te remaining", round(60 - (stop - start)), "seconds before continuing")
            time.sleep(60 - (stop - start) + 1)
            start = time.time()

    print("Add batch of Movies")
    batch_callback(client.batch.create_objects())
    client.batch.empty_objects()
        
    # add the crefs
    print("Add crefs")
    for movie in data:
        client.batch(batch_size=1000, dynamic=True)
        for director in split_items("Director", movie):
            client.batch.add_reference(generate_uuid(movie["Title"]), "Movie", "director", generate_uuid(director.strip()))
            client.batch.add_reference(generate_uuid(director.strip()), "Director", "movies", generate_uuid(movie["Title"]))
        for actor in split_items("Cast", movie):
            client.batch.add_reference(generate_uuid(movie["Title"]), "Movie", "cast", generate_uuid(actor.strip()))
            client.batch.add_reference(generate_uuid(actor.strip()), "Cast", "movies", generate_uuid(movie["Title"]))
        for genre in split_items("Genre", movie):
            client.batch.add_reference(generate_uuid(movie["Title"]), "Movie", "genre", generate_uuid(genre.strip()))
    client.batch.create_references()
    print('done')

def print_usage() -> None:
    """
    Print command-line interface description.
    """

    print("Usage: ./import.py <WEAVIATE_URL> <BATCH_SIZE (OPTIONAL)>")

def main():
    """
    The main function that is executed when running this script.
    """

    nr_argv = len(sys.argv)

    if nr_argv not in (2, 3):
        print(
            f"ERROR: Please provide your Weaviate url as one argument and an optional batch_size.")
        print_usage()
        sys.exit(1)

    main_client = Client(sys.argv[1])
    wait_time_limit = 240
    while not main_client.is_ready():
        if not wait_time_limit:
            sys.stderr.write("\rTIMEOUT: Weaviate not ready. \
                            Try again or check if weaviate is running.\n")
            sys.exit(1)
        sys.stdout.write(
            f"\rWait for weaviate to get ready. {wait_time_limit:02d} seconds left.")
        sys.stdout.flush()
        wait_time_limit -= 2
        time.sleep(2.0)

    # Empty the Weaviate
    main_client.schema.delete_all()

    if not main_client.schema.contains():
        print(f"Creating Schema")
        dir_path = os.path.dirname(os.path.realpath(__file__))
        schema_file = os.path.join(dir_path, "schema.json")
        main_client.schema.create(schema_file)
        print(f"Creating Schema done")

    print(f"Importing data from dataset based on batch size:", int(sys.argv[2]))
    if nr_argv == 3:
        upload_data_to_weaviate(
            client=main_client,
            batch_size=int(sys.argv[2])
        )
    else:
        upload_data_to_weaviate(
            client=main_client,
            batch_size=100
        )


if __name__ == "__main__":
    main()

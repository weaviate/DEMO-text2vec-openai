#!/usr/bin/env python3
"""
Import data into weaviate script.
"""
import os
import sys
import json
import time
from typing import Callable, Optional
from weaviate import Client
from load.data import Loader

def upload_data_to_weaviate(data: json, callback: Callable[[dict], None]) -> None:
    """
    Call function to upload data to Weaviate.
    Parameters
    ----------
    data : json
        JSON file with the data.
    callback : Callable[[dict], None]
        The callback function used on the JSON file.
    """

    with open(data) as file:
        data = json.load(file)
        callback(data)

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

    with client.batch as batch:
        loader = Loader(batch)

        f = open('data/movies.json')
        data = json.load(f)
        
        for movie in data:
            loader.load_movie(data)

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
    if nr_argv not in (1,2):
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

    if not main_client.schema.contains():
        print(f"\nCreating Schema")
        dir_path = os.path.dirname(os.path.realpath(__file__))
        schema_file = os.path.join(dir_path, "schema.json")
        main_client.schema.create(schema_file)
        print(f"\nCreating Schema done")

    print(f"\nImporting data from")
    if nr_argv == 2:
        upload_data_to_weaviate(
            client=main_client,
            batch_size=int(sys.argv[2])
        )
    else:
        upload_data_to_weaviate(
            client=main_client,
            batch_size=200
        )


if __name__ == "__main__":
    main()
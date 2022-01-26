"""
A Loader class to import data into weaviate.
"""
import uuid
from typing import Optional
from weaviate.batch import Batch


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


class Loader:
    """
    A Loader class that uploads Movies, Actors, Directors and Genres.
    It makes use of the weaviate.batch.Batch to upload data in batches.
    """

    def __init__(self, batch: Batch):
        self.batch = batch

    def load_movie(self, data: dict) -> None:
        """
        Load a Movie into weaviate.
        Parameters
        ----------
        data : dict
            Raw Movie data.
        """

        movie_id = generate_uuid(data['Title'])

        ## TO DO: 
        # check if actors, genres and directors exist as classes, if not create one. Make sure to use process_input. 
        # add the movie with the props

        ##### ADD ACTORS #####

        ##### ADD DIRECTORS #####

        ##### ADD GENRES #####

        ##### ADD MOVIE #####



def process_input(key, value: str) -> str:
    """
    Clean up the data.
    Parameters
    ----------
    key: str
        Which key the object(see value) to clean belongs to.
    value: str
        The object to clean.
    Returns
    -------
    str
        Cleaned object.
    """

    if value == 'unknown':
        return ''

    if key == 'Plot':
        value = value.replace('\n', ' ')
    elif key == 'Cast':
        value = value.split(',')
    elif key == 'Director':
        value = value.split(',')
    elif key == 'Genre':
        value = value.split(',')
    elif key == 'Origin/Ethnicity':
        value = value.split(',')
    elif key == 'Origin/Ethnicity':
        value = value.split(',')
    return value
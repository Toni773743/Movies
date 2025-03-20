from random import random
from faker import Faker

fake = Faker()

class DataGenerator:
    @staticmethod
    def movie_data():
        return {
            "name": fake.sentence(nb_words=3),
            "imageUrl": fake.image_url(),
            "price": fake.random_int(min=50, max=500),
            "description": fake.text(),
            "location": "MSK",
            "published": fake.boolean(),
            "genreId": fake.random_int(min=1, max=10)
        }



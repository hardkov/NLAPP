import unittest

from nlapp.data_model.dataset_format import DatasetFormat
from nlapp.service.datasets.mappers.user.text_classification_mapper import (
    TextClassificationMapper,
)


class TestTextClassificationMapper(unittest.TestCase):
    def test_parse_json_when_contains_object(self):
        # given
        data_from_user = {
            "data": [
                {
                    "content": "My lovely Pat has one of the GREAT voices of her generation. I have listened to this "
                               "CD for YEARS and I still LOVE IT. When I'm in a good mood it makes me feel better. A "
                               "bad mood just evaporates like sugar in the rain. This CD just oozes LIFE. Vocals are "
                               "jusat STUUNNING and lyrics just kill. One of life's hidden gems. This is a desert "
                               "isle CD in my book. Why she never made it big is just beyond me. Everytime I play "
                               "this, no matter black, white, young, old, male, female EVERYBODY says one thing ",
                    "class": "1",
                },
                {
                    "content": "A complete waste of time. Typographical errors, poor grammar, and a totally pathetic "
                               "plot add up to absolutely nothing. I'm embarrassed for this author and very "
                               "disappointed I actually paid for this book.",
                    "class": "0",
                },
            ]
        }
        mapping_columns = {
            "text": "data.content",
            "label": "data.class",
        }
        mapper = TextClassificationMapper(mapping_columns)

        # when
        mapped_data = mapper.map(data_from_user, DatasetFormat.JSON)

        for c, l in zip(mapped_data.get("text"), mapped_data.get("label"), ):
            print(c)
            print(l)
            print()

        # then
        self.assertEqual(len(mapped_data.get("text")), 2)
        self.assertEqual(len(mapped_data.get("label")), 2)

    def test_parse_json_when_contains_array(self):
        # given
        data_from_user = {
            "sentence": [
                "Wall St. Bears Claw Back Into the Black  NEW YORK (Reuters) - Short-sellers, Wall Street's dwindling "
                "band of ultra-cynics, are seeing green again. ",
                "Quality Gets Swept Away Quality Distribution is hammered after reporting a large loss for the second "
                "quarter."
            ],
            "tag": ["1", "2"],
        }

        mapping_columns = {
            "text": "sentence",
            "label": "tag",
        }
        mapper = TextClassificationMapper(mapping_columns)

        # when
        mapped_data = mapper.map(data_from_user, DatasetFormat.JSON)

        # then
        self.assertEqual(
            mapped_data.get("text"), data_from_user.get("sentence")
        )

        self.assertEqual(mapped_data.get("label"), data_from_user.get("tag"))

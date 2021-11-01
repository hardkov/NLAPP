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
                    "premise": "The cat sat on the mat.",
                    "hypothesis": "The cat did not sit on the mat.",
                    "label": "0",
                    "id": "0",
                },
                {
                    "premise": "When you've got no snow, it's really hard to learn a snow sport so we looked at all the different ways I could mimic being on snow without actually being on snow.",
                    "hypothesis": "When you've got snow, it's really hard to learn asnow sport so we looked at all the different ways I could mimic being on snow without actually being on snow.",
                    "label": "0",
                    "id": "1",
                },
            ]
        }
        mapping_columns = {
            "sentence1": "data.premise",
            "sentence2": "data.hypothesis",
            "label": "data.label",
            "idx": "data.id",
        }
        mapper = TextClassificationMapper(mapping_columns, 2, True)

        # when
        mapped_data = mapper.map(data_from_user, DatasetFormat.JSON)

        for s1, s2, l, i in zip(
            mapped_data.get("sentence1"),
            mapped_data.get("sentence2"),
            mapped_data.get("label"),
            mapped_data.get("idx"),
        ):
            print(s1)
            print(s2)
            print(l)
            print(i)
            print()

        # then
        self.assertEqual(len(mapped_data.get("sentence1")), 2)
        self.assertEqual(len(mapped_data.get("sentence2")), 2)
        self.assertEqual(len(mapped_data.get("label")), 2)
        self.assertEqual(len(mapped_data.get("idx")), 2)

    def test_parse_json_when_contains_array(self):
        # given
        data_from_user = {
            "title": ["Great CD", "Coal is using to produce [MASK] energy."],
            "content": [
                "My lovely Pat has one of the GREAT voices of her generation. I have listened to this CD for YEARS and I still LOVE IT. When I'm in a good mood it makes me feel better. A bad mood just evaporates like sugar in the rain. This CD just oozes LIFE. Vocals are jusat STUUNNING and lyrics just kill. One of life's hidden gems. This is a desert isle CD in my book. Why she never made it big is just beyond me. Everytime I play this, no matter black, white, young, old, male, female EVERYBODY says one thing "
                "Who was that singing ?"
                "",
                "Check out Maha Energy's website. Their Powerex MH-C204F charger works in 100 minutes for rapid charge, with option for slower charge (better for batteries). And they have 2200 mAh batteries.",
            ],
            "label": ["1", "2"],
        }

        mapping_columns = {
            "sentence1": "title",
            "sentence2": "content",
            "label": "label",
        }
        mapper = TextClassificationMapper(mapping_columns, 2, False)

        # when
        mapped_data = mapper.map(data_from_user, DatasetFormat.JSON)

        # then
        self.assertEqual(
            mapped_data.get("sentence1"), data_from_user.get("title")
        )
        self.assertEqual(
            mapped_data.get("sentence2"), data_from_user.get("content")
        )
        self.assertEqual(mapped_data.get("label"), data_from_user.get("label"))

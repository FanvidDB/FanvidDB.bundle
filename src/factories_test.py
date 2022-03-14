import uuid

import factory


class FanvidFactory(factory.Factory):
    class Meta:
        model = dict

    uuid = factory.LazyFunction(uuid.uuid4)
    title = factory.Faker("words", nb=5)
    summary = factory.Faker("sentences", nb=3)
    rating = "gen"
    premiere_date = factory.Faker("date")
    thumbnail_url = "https://tile.loc.gov/storage-services/service/pnp/cph/3c00000/3c00000/3c00100/3c00170_150px.jpg#h=150&w=121"  # noqa: E501
    length = 200
    creators = ["vidder1"]


class MockMetadata:
    def __init__(self):
        self.art = {}
        self.posters = {}

from datetime import datetime
from googletrans import Translator

import weaviate
from tqdm import tqdm
import json

#streamlit connection address and port are defined in docker compose files
client = weaviate.Client("http://localhost:8080", timeout_config=(4, 60))

#Schema definition with thesis class
schema = {"classes": [
    {
        "class": "Thesis",
        "properties": [
            {
                "name": "name",
                "dataType": ["string"],
            }, {
                "name": "ext_id",
                "dataType": ["string"],
                "moduleConfig": {
                    "text2vec-contextionary": {
                    "skip": True, #don't use this property when vectorizing
                    }
                }
            }, {
                "name": "lang",
                "dataType": ["string"],
                "moduleConfig": {
                    "text2vec-contextionary": {
                    "skip": True, #don't use this property when vectorizing
                    }
                }
            }
        ]
    }
]}

client.schema.delete_all()
client.schema.create(schema)

class RequestCounter:
    count: int = 0
    time: datetime = datetime.now()

    def __call__(self, results):
        self.count += len(results)
        print(f"{len(results):10} created, {self.count:15} so far in {datetime.now() - self.time}")

translator = Translator()

with client.batch(batch_size=2048, callback=RequestCounter(), timeout_retries=8) as batch:
    with open('dataset.json', 'r') as f:
        dataset = json.load(f)

    #sanity check
    assert len(dataset['_id'].values()) == len(dataset['name'].values()) == len(dataset['lang'].values())

    multilang = False

    for id, name, lang in tqdm(zip(dataset['_id'].values(), dataset['name'].values(), dataset['lang'].values()), total = len(dataset['_id'].values())):
        if not multilang and lang != 'en':
            translation = translator.translate(name)
            name = translation.text

        object = {
            "name": name,
            "ext_id": id,
            "lang": lang
        }

        client.data_object.create(
            data_object = object,
            class_name = "Thesis"
        )

client.schema.get() # get the full schema as example

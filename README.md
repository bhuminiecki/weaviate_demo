# weaviate_demo
A simple weaviate demo used for thesis deduplication

## weaviate
Weaviate documentation can be found [here](https://www.semi.technology/developers/weaviate/current/).

## compose
Compose files included in this project contain different presets for weaviate install
- docker-compose.yml - default preset, big 768d english language model with no NER component.
- docker-compose-en.yml - small 384d english language model with no NER component.
- docker-compose-multilang.yml - small 384d mutilanguage language model with no NER component.
- docker-compose-big-ner.yml - big 768d english language model with NER component.
- docker-compose-small-ner.yml - small 384d english language model with NER component.

## usage

Install requirements:
```
pip install -r requirements.txt
```

Run docker compose of your choice
```
cd compose

docker-compose [-f filename] up -d
```

Prepare your dataset.json file.

Run the indexer
```
python3 index.py
```

Start the aplication
```
streamlit run streamlit_client.py
```

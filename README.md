# Andaluh-api

Python-Flask API to serve [andaluh-py](https://github.com/andalugeeks/andaluh-py): the español (spanish) spelling to andaluz proposals transliteration package.

## Table of Contents

- [Description](#description)
- [Usage](#usage)
- [Running](#running)
- [Roadmap](#roadma)
- [Support](#support)
- [Contributing](#contributing)

## Description

The **Andalusian varieties of [Spanish]** (Spanish: *andaluz*; Andalusian) are spoken in Andalusia, Ceuta, Melilla, and Gibraltar. They include perhaps the most distinct of the southern variants of peninsular Spanish, differing in many respects from northern varieties, and also from Standard Spanish. Further info: https://en.wikipedia.org/wiki/Andalusian_Spanish.

This application provides with a basic python-flask API for [andaluh-py](https://github.com/andalugeeks/andaluh-py). Further info: https://github.com/andalugeeks/andaluh-py

## Usage

The API only provides one GET /epa method, so far. It transliterates español (spanish) to [andaluz EPA](https://andaluhepa.wordpress.com) proposal. It is published on port 5000 (Python-FLASK default port). Output is encoded with unicode.

```
$ curl -X GET "http://localhost:5000/epa?texto=El veloz murciélago hindú comía feliz cardillo y kiwi. La cigüeña tocaba el saxofón detrás del palenque de paja." 
{"El veloz murci\u00e9lago hind\u00fa com\u00eda feliz cardillo y kiwi. La cig\u00fce\u00f1a tocaba el saxof\u00f3n detr\u00e1s del palenque de paja.": "Er bel\u00f4h mur\u00e7i\u00e9lago ind\u00fa com\u00eda fel\u00eeh cardiyo y kiwi. La \u00e7igue\u00f1a tocaba er \u00e7\u00e2\u00e7\u00e7of\u00f3n detr\u00e2h der palenque de paha."}
```

GET /epa method accepts two parameters:

* **vaf** (voiceless alveolar fricative /s/): Use it to enforce seseo (assign "s"), zezeo (assign "z") or heheo (assign "h") instead of cedilla.
* **vvf** (voiceless velar fricative /x/): Use it to keep /x/ sounds as J instead of /h/ by assigning "j".

```
$ curl -X GET "http://localhost:5000/epa?texto=El veloz murciélago hindú comía feliz cardillo y kiwi. La cigüeña tocaba el saxofón detrás del palenque de paja.&vaf=z&vvf=j"
{"El veloz murci\u00e9lago hind\u00fa com\u00eda feliz cardillo y kiwi. La cig\u00fce\u00f1a tocaba el saxof\u00f3n detr\u00e1s del palenque de paja.": "Er bel\u00f4h murzi\u00e9lago ind\u00fa com\u00eda fel\u00eeh cardiyo y kiwi. La zigue\u00f1a tocaba er z\u00e2zzof\u00f3n detr\u00e2h der palenque de paja."}
```

## Running

Directly

```
$ pip install -r requirements.txt
$ python app/server.py
```

Dockerised

```
$ docker-compose up --build -d
```

## Roadmap

* Migrating to python3
* Adding kong as api management tool

## Support

Please [open an issue](https://github.com/andalugeeks/andaluh-api/issues/new) for support.

## Contributing

Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and open a pull request.

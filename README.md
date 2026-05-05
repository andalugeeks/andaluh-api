# Andaluh API

Python Flask API for [andaluh-py](https://github.com/andalugeeks/andaluh-py), with optional verb conjugation powered by [andaluh-verbs](https://github.com/andalugeeks/andaluh-verbs).

## Table of Contents

- [Description](#description)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Running](#running)
- [Support](#support)
- [Contributing](#contributing)

## Description

The **Andalusian varieties of Spanish** (Spanish: *andaluz*; Andalusian) are spoken in Andalusia, Ceuta, Melilla, and Gibraltar. They include perhaps the most distinct of the southern variants of peninsular Spanish, differing in many respects from northern varieties, and also from Standard Spanish. Further info: https://en.wikipedia.org/wiki/Andalusian_Spanish.

This application exposes a basic HTTP API for:

- transliterating Spanish text to Andaluh EPA with `andaluh-py`
- optionally returning Andaluh verb conjugations with `andaluh-verbs`

Further info: https://github.com/andalugeeks/andaluh-py

## Usage

The API currently provides one `GET /epa` endpoint. It transliterates Spanish text to the [Andaluh EPA](https://andaluhepa.wordpress.com) proposal and can also return verb conjugations. When running locally or with Docker Compose, the service is available on port `5000`.

```bash
$ curl "http://localhost:5000/epa?spanish=El%20veloz%20murci%C3%A9lago%20hind%C3%BA%20com%C3%ADa%20feliz%20cardillo%20y%20kiwi."
{"spanish":"El veloz murciélago hindú comía feliz cardillo y kiwi.","andaluh":"Er belôh murçiélago indú comía felîh cardiyo y kiwi.","rules":{"vaf":"ç","vvf":"h","escapeLinks":false,"conjugate":false}}
```

`GET /epa` accepts these query parameters:

| Parameter | Required | Values | Description |
| --- | --- | --- | --- |
| `spanish` | Yes | Any text | Spanish text to transliterate. |
| `vaf` | No | `ç`, `z`, `s`, `h` | Voiceless alveolar fricative `/s/` variant. Use `ç` for çeçeo, `z` for zezeo, `s` for seseo or `h` for heheo. |
| `vvf` | No | `h`, `j` | Voiceless velar fricative `/x/` variant. Use `j` to preserve the sound as `j`; defaults to `h`. |
| `escapeLinks` | No | `true`, `false`, `True`, `False` | When true, URLs, hashtags and mentions are not transliterated. |
| `conjugate` | No | `true`, `false`, `True`, `False` | When true, the response includes conjugation data from `andaluh-verbs`. |

```bash
$ curl "http://localhost:5000/epa?spanish=El%20veloz%20murci%C3%A9lago%20hind%C3%BA%20com%C3%ADa%20feliz%20cardillo%20y%20kiwi.&vaf=z&vvf=j"
{"spanish":"El veloz murciélago hindú comía feliz cardillo y kiwi.","andaluh":"Er belôh murziélago indú comía felîh cardiyo y kiwi.","rules":{"vaf":"z","vvf":"j","escapeLinks":false,"conjugate":false}}
```

Use `escapeLinks=true` to leave links, mentions and hashtags unchanged:

```bash
$ curl "http://localhost:5000/epa?spanish=Visita%20https%3A%2F%2Fandaluh.es%20y%20menciona%20%40andalugeeks%20%23andaluh&escapeLinks=true"
```

Use `conjugate=true` to include verb conjugation data. If the verb cannot be conjugated, the API returns a `conjugation_error` field instead.

```bash
$ curl "http://localhost:5000/epa?spanish=jocifar&conjugate=true"
{"spanish":"jocifar","andaluh":"hoçifâh","rules":{"vaf":"ç","vvf":"h","escapeLinks":false,"conjugate":true},"conjugation":{"infinitibo":["hoçifâh"]}}
```

## API Documentation

Swagger UI is available at:

```text
http://localhost:5000/docs
```

The OpenAPI/Swagger definition is maintained in [`swagger.json`](swagger.json).

A sample Postman collection with example requests and responses is available at [`postman_collection.json`](postman_collection.json).

## Running

Directly

```bash
$ pip install -r requirements.txt
$ python3 app/server.py
```

Dockerised

```bash
$ docker-compose up --build -d
```

Notes:

- The project currently targets Python `3.12`.
- The Docker image prebuilds the Spanish `verbecc` model during `docker-compose build` so conjugation works at runtime without writing into `site-packages`.

## Support

Please [open an issue](https://github.com/andalugeeks/andaluh-api/issues/new) for support.

## Contributing

Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and open a pull request.

# exchange

[![Build status](https://badge.buildkite.com/bc9b5a1bc6891fbf8feca7e8f8dfd7508136b2720daf16a771.svg)](https://buildkite.com/drizzle/exchange)
[![codecov](https://codecov.io/gh/drizzleco/exchange/branch/master/graph/badge.svg?token=D91AS5EED0)](https://codecov.io/gh/drizzleco/exchange)

## Requirements

- Python 3
- npm
- docker
- Heroku CLI (optional)

## Getting Started

1. `make install`
2. `make start`

## Docker

To run a local copy of the code, run the following

```bash
docker-compose up -d
```

## Heroku

If you want to deploy with heroku and you have the CLI, the following steps are sufficient:

```
0. heroku create  # one time
1. heroku container:push web
2. heroku container:release web
3. heroku open
```

## Usage

### `make help` or `make`

display help message for useful snippets!

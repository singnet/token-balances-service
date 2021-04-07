# token-balances-service

Backend for the token balances DApp

Install the dependencies and devDependencies and start the serve locally.

```sh
npm install -g serverless # Install serverless
npm install --save-dev
```

Configure database from `common/config.py`

```sh
pip3 install -r requirements.txt
alembic upgrade head # Sync database tables
```

## Requirements

| Language     | Min Version                       |
| ------------ | --------------------------------- |
| Python 3.8   | https://www.python.org/downloads/ |
| Node JS 12.X | https://nodejs.org/en/            |

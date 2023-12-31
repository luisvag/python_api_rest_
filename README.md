# Flask REST API + React

Project aiming to learn about backend/frontend process to login
By luisvag, Gabriel Marcano

## API Reference

#### Get all users

`GET /users`

#### Get user info

`GET /user/{id}`

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of user to fetch |

#### Register new user

`POST /create-user`

Example JSON body:

```json
{
  "username": "John",
  "password": 123
}
```

#### Change user password

`PATCH /reset-password`

Example JSON body:

```json
{
  "username": "John",
  "password": 456
}
```

## Run Locally

Clone the project

```bash
  git clone https://github.com/luisvag/python_api_rest_.git
```

Go to the project directory

```bash
  cd python_api_rest_
```

### API

Go to the api directory

```bash
  cd api
```

Start the server

```bash
  python main.py
```

### Front

Go to the client directory

```bash
  cd client
```

Install dependencies

```bash
  npm install
```

Start the server

```bash
  npm run dev
```

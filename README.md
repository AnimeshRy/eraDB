<h1 align="center">🍿 EraDB</h1>
<p align="center">Movie Database with Django and Bootstrap 4</p>
<p align="center">
<img alt="APM" src="https://img.shields.io/apm/l/vim-mode">
<img alt="GitHub Pipenv locked Python version" src="https://img.shields.io/github/pipenv/locked/python-version/AnimeshRy/eraDB">
<a href="https://github.com/AnimeshRy/eraDB/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/AnimeshRy/eraDB"></a>
<a href="https://github.com/AnimeshRy/eraDB/network"><img alt="GitHub forks" src="https://img.shields.io/github/forks/AnimeshRy/eraDB"></a>

<p align="center">
    <a href="https://youtu.be/rCxIc5Z1YAA">
  <img width="460" height="300" src="./static/img/result.gif">
    </a>
</p>

## ⚡ Features

🎯 **OMDb API** - Utilize the extensive omDB API

🎯 **Inject MovieData** - Inject Movie Data if not locally available

🎯 **WatchList** - Add and manage movies, series etc to seperate user watchlist

🎯 **Sort by Actor's and Genre's** - Sort locally movie data based on actor and genre.

🎯 **Reviews and Comments** - Add a review for a movie and other users can like, dislike or comment on the review.

## 🚀 Setup

These instructions will get you a copy of the project up and running on your local machine for deployement and development.

You'll need [Git](https://git-scm.com) and [Python 3.8+](https://www.python.org/downloads/) installed on your local computer.

```
python@3.8 or higher
git@2.17.1 or higher
```

You can also use the [Zip](https://github.com/AnimeshRy/gymrocket/archive/master.zip) file and extract the folder.

## 🔧 How To Use

From your command line, clone and deploy:

```bash
# Clone this repository
$ git clone git@github.com:AnimeshRy/eraDB.git

# Go into the repository
$ cd eraDB

# Install dependencies
# if Pipenv available ? run
$ pipenv install

# Else
$ pip install -r requirements.txt

```

## 📨 Environment Setup

```bash
# You need some environment variables to setup.
touch .env
# replace string with a random string
SECRET_KEY={string}
DEBUG=True
omdbKey={omdbAPIKey}

# Create media directory
mkdir media
```

Get your omdb API Key from [here.](http://www.omdbapi.com/)

## 🛠️ Django Setup

After installing the requirements, we'll need to setup some Django commands.

### Perform database migration:

```bash
python manage.py check
python manage.py migrate
```

### To Create Admin Account

> You can also create a account from the Signup page

```bash
python manage.py createsuperuser
# follow instruction
```

### Run Development Server

```bash
python manage.py runserver
```

Navigate to [http://localhost:8000/](http://localhost:8000/) endpoint in your browser.

Admin endpoint is at http://127.0.0.1:8000/admin/

## 📄 License

This project is licensed under the MIT License - see the [LICENSE.md](./LICENSE) file for details

## Important

- This project is just meant as a little side project and is not meant as a disrespect towards existing movie databases.

- The project will not be maintained, anyone can clone and have fun with it.

- **There isn't any point in deploying this app as the API calls are limited and the database gets populated very fast based on every unique movie click**.

## 👨‍💻 Thanks

- [OMDb API](http://www.omdbapi.com/)
- [Bootstrap 4](https://getbootstrap.com/)
- [Django 3](https://docs.djangoproject.com/en/3.1/releases/3.0/)
- [SQLite3](https://www.sqlite.org/index.html)

#### Designed & Developed with 💙 by [Animesh Singh](https://www.github.com/AnimeshRy)

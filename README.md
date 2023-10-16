# online_restaurant
Description:

An online restaurant where you can view food and order it, paying its cost using a card. Restaurant employees also have additional opportunities to create dishes. The site also has a forum where you can create posts about dishes and comments on them. There is also a system for assessing the quality of dishes, email address verification, a page with customer orders and the ability to log in to the site using GitHub.

## Check it out!

[online_restaurant deployed to Render](https://online-restaurant.onrender.com/)
  

  ## Installation
###### (example for macos)

Python3 must be already installed and postgres_db must be created 

```shell
git clone https://github.com/Paul-Starodub/online_restaurant
cd online_restaurant
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
brew services start postgresql
brew services start redis
celery -A online_restaurant worker -l INFO
stripe listen --forward-to localhost:8000/webhook/stripe/
python manage.py runserver
```

## Features

- Authentication for user via forms or via GitHub
- Manage the creation of food orders using your personal account and shopping cart. Payment by credit card. Creation of reviews on the quality of the dish and comments on it, a system of likes.
- Powerful admin panel for advanced managing 


## Demo

Use the following command to load prepared data from fixture to get demo access to the system:

  `python manage.py loaddata restaurant_data.json`.

After loading data from fixture you can use following users (or create another one by yourself):

  - Login: `admin` (superuser) 
  - Password: `vovk7777`
---
  - Login: `red` (staff)
  - Password: `vovk7777`
 ---
  - Login: `green`
  - Password: `vovk7777`

You can absolutely safely check payment for orders in test mode using `stripe` with `card information` 4242424242424242, `MM/VV` - any date in the future, `CVC` - any three digits, `cardholder name` - any name  

After cloning, you need to create your `.env` file and register your variables in it. After that, everything will work. For an example, see the file `.env.sample`

![Website interface](/static/css/clipboard_image_234cd88ae65.png)
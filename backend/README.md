# Temari Share API

## Installation
```bash
# Python 3 and MySQL development headers and libraries
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
pip install mysqlclient

# set up database(edit setup_db.sql to set up different user)
cat setup_db.sql | mysql -u root -p

# create and activate virtual environment
python3 -m venv .venv
. .venv/bin/activate

pip install -r requirements.txt
flask run
```
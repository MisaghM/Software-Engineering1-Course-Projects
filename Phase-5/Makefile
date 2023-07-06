PROJECT_DIR = SaPaMi

DATABASE = $(PROJECT_DIR)/db.sqlite3

.PHONY: all clean run test

all: $(DATABASE)

clean:
	rm -f $(DATABASE) >/dev/null 2>&1

run: $(DATABASE)
	cd $(PROJECT_DIR) && ./manage.py runserver

test:
	cd $(PROJECT_DIR) && ./manage.py test

$(DATABASE):
	cd $(PROJECT_DIR) && ./manage.py migrate

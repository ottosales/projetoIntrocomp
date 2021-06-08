all: up

up:
	python3 src/main.py
clean:
	rm -r src/__pycache__
install:
	python3 -m pip install pygame==2.0.0
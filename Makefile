.PHONY: setup run

setup:
    @echo "Setting up the game..."
    pip install -r requirements.txt

run:
    python src/snake.py
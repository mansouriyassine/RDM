from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

# Configuration du jeu
GRID_SIZE = 20
INITIAL_SNAKE = [(GRID_SIZE // 2, GRID_SIZE // 2)]
INITIAL_DIRECTION = 'RIGHT'

# Variables globales du jeu
snake = INITIAL_SNAKE.copy()
direction = INITIAL_DIRECTION
food = None

def generate_food():
    global food
    while True:
        new_food = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        if new_food not in snake:
            food = new_food
            break

@app.route('/')
def index():
    return render_template('index.html', grid_size=GRID_SIZE)

@app.route('/start', methods=['POST'])
def start_game():
    global snake, direction, food
    snake = INITIAL_SNAKE.copy()
    direction = INITIAL_DIRECTION
    generate_food()
    return jsonify({"snake": snake, "food": food})

@app.route('/move', methods=['POST'])
def move():
    global snake, direction, food
    
    new_direction = request.json['direction']
    if new_direction != 'NONE':
        direction = new_direction
    
    head = snake[0]
    if direction == 'UP':
        new_head = ((head[0] - 1) % GRID_SIZE, head[1])
    elif direction == 'DOWN':
        new_head = ((head[0] + 1) % GRID_SIZE, head[1])
    elif direction == 'LEFT':
        new_head = (head[0], (head[1] - 1) % GRID_SIZE)
    elif direction == 'RIGHT':
        new_head = (head[0], (head[1] + 1) % GRID_SIZE)
    
    if new_head in snake:
        return jsonify({"game_over": True})
    
    snake.insert(0, new_head)
    
    if new_head == food:
        generate_food()
    else:
        snake.pop()
    
    return jsonify({"snake": snake, "food": food, "game_over": False})

if __name__ == '__main__':
    generate_food()
    app.run(debug=True)
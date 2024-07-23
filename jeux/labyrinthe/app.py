from flask import Flask, render_template, jsonify
from random import randint
import os

app = Flask(__name__)

def generate_maze(width, height):
    # Le code de génération du labyrinthe reste inchangé
    maze = [[1 for _ in range(width)] for _ in range(height)]
    
    def carve_path(x, y):
        maze[y][x] = 0
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dx, dy in directions:
            nx, ny = x + dx*2, y + dy*2
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 1:
                maze[y+dy][x+dx] = 0
                carve_path(nx, ny)
    
    start_x, start_y = randint(0, width-1), randint(0, height-1)
    carve_path(start_x, start_y)
    
    maze[0][0] = 2  # Entrée
    maze[height-1][width-1] = 3  # Sortie
    
    return maze

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_maze')
def get_maze():
    maze = generate_maze(15, 15)
    return jsonify(maze)

if __name__ == '__main__':
    app.run(debug=True)
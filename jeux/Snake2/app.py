from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Simulated leaderboard data (replace with database in a real application)
leaderboard = [
    {"name": "Nancy", "score": 100},
    {"name": "Ellen", "score": 80},
    {"name": "Bob", "score": 60},
    {"name": "Tom", "score": 40},
    {"name": "Alice", "score": 20},
]

@app.route('/')
def index():
    return render_template('game.html')

@app.route('/leaderboard')
def show_leaderboard():
    return render_template('leaderboard.html', scores=leaderboard)

@app.route('/submit_score', methods=['POST'])
def submit_score():
    data = request.json
    name = data.get('name')
    score = data.get('score')
    
    # In a real application, you would save this to a database
    leaderboard.append({"name": name, "score": score})
    leaderboard.sort(key=lambda x: x["score"], reverse=True)
    leaderboard = leaderboard[:5]  # Keep only top 5 scores
    
    return jsonify({"message": "Score submitted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
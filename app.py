from flask import Flask, request, jsonify, send_file
import rdm3

app = Flask(__name__)

@app.route('/')
def index():
    return send_file('affichage.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.form
    results = rdm3.analyze_poutre(data)
    return jsonify({
        'message': results['message'],
        'image_url': '/resultats_poutre.png'
    })

@app.route('/resultats_poutre.png')
def get_image():
    return send_file('resultats_poutre.png', mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
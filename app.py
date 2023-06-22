from main import create_app
from config.default import ProConfig

app = create_app(ProConfig)

@app.route('/swagger_file')
def swagger_file():
    return app.send_static_file('swagger.json')

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")
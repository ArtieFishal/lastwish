from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return '''
    <html>
    <head><title>LastWish Test</title></head>
    <body>
        <h1>LastWish Platform - Test Deployment</h1>
        <p>This is a test to verify the deployment is working.</p>
        <p>The full LastWish platform will be deployed shortly.</p>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


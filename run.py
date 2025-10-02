from app.main import app

if __name__ == '__main__':
    # debug=True удобен при разработке
    app.run(host='127.0.0.1', port=5000, debug=True)
from waitress import serve
from app import app  # замени your_application на имя твоего main файла Flask

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
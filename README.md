🚀 FastAPI Project

A simple and scalable backend API built using FastAPI. This project demonstrates how to create high-performance APIs with modern Python features.

📌 Features
⚡ Fast and high-performance API
🧠 Built with Python type hints
📦 Easy to scale and maintain
🔄 Automatic interactive API docs
🛠️ Clean and structured code
🛠️ Tech Stack
Python 3.x
FastAPI
Uvicorn

.
├── main.py          # Entry point of the application
├── requirements.txt # Dependencies
└── README.md        # Project documentation

⚙️ Installation
Clone the repository:
git clone https://github.com/lazymcmod/FastAPI.git
Navigate to the project folder:
cd your-repo-name
Create a virtual environment:
python -m venv venv
Activate the environment:
Windows:
venv\Scripts\activate
Mac/Linux:
source venv/bin/activate
Install dependencies:
pip install -r requirements.txt
▶️ Running the Server
uvicorn main:app --reload

Server will run at:

http://127.0.0.1:8000
📖 API Documentation

FastAPI automatically provides interactive docs:

Swagger UI:
http://127.0.0.1:8000/docs
ReDoc:
http://127.0.0.1:8000/redoc
📌 Example Code
```bash
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}
```
🤝 Contributing

Contributions are welcome! Feel free to fork the repo and submit a pull request.

📄 License

This project is open-source and available under the MIT License.

✨ Author

LazyMcmod

# Local private MySQL API

New version of the locally running API for MySQL DB

# Dev

## VS Code Run  

```json
{
    "name": "Python: Connexion",
    "type": "python",
    "request": "launch",
    "module": "connexion",
    "cwd": "${workspaceFolder}",
    "env": {
        "FLASK_APP": "app.py",
        "FLASK_ENV": "development",
        "FLASK_DEBUG": "1"
    },
    "args": [
        "run",
        "swagger.yaml",
        "--port",
        "5678"
    ],
    "jinja": true
} 
```  

## READ?? 
https://levelup.gitconnected.com/how-to-create-a-python-api-using-flask-connexion-4f3fc77e7f6e
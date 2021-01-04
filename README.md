```bash
pip3 install Flask
git clone {repo url}
cd unity-flask-api
python3 app.py
```


**POST /api/saveData**

| Key  |  |
| ------------- | ------------- |
| user_id  | (must be uniqe) |
| level  | |
| timestamp  | (must be uniqe) |
| pressKey  | |
| pressTime  | |
| box  | |
| boolStatus  | |

Returns current user's data as Json with HTTP status code 201.
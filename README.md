# Test Run (locally) 
`poetry run python cli.py test main.py`

# POST req. response

POST `http://localhost:4000/chat`

```
body:
{
  "messages": [
    {"text": "Hi, I want to know if its possible to read 10 books at once.", "sender": "user"},
    {"text": "I wanted to know if there's a way to book cheaper flights", "sender": "user"},
    {"text": "What's the weather like today?", "sender": "user"}
  ]
}
```
![demo](textbase/frontend/public/demo.png)




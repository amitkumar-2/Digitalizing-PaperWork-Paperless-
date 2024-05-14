from cricket import create_app, create_tocken

app=create_app()

token = create_tocken(username='amitkumar')
print(token)

if __name__ == "__main__":
    app.run(debug=True)
from website import create_app
from website.models import User
from flask_login import login_user

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)



    
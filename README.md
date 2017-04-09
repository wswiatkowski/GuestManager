GuestManager 0.1 by wswiatkowski

1. Prerequisites

    pip packages:
    - flask
    - flask_api
    - psycopg2
    
    db:
    - PostgreSQL

    recommended:
    - Postman

2. First run
    - Make sure that your PostgreSQL database is set up and configured as in ./DbConnection.py file.
    - Run ./run.sh to define needed environment variable and run Flask server
    - Open Postman and set URL to http://localhost:5000/invitation
    - Simply PUT, POST, DELETE or GET invitees to your guest list

3. Methods explanation

All methods accepts only application/json input, and responds with (JSON output/error message) and response code.
    - PUT(name, email)
      Creates user from scratch no matter what.

    - POST(name, email)
      It updates user if user with exactly the same name or email is existing, if not - then
      creates new one just like PUT method. Returns error if more than one invitee is going to be updated.

    - DELETE(name, email)
      Deletes all existences of invitees with exactly the same name and email as given in parameter.

    - GET()
      Responds with whole guest list with their names and emails in JSON format.

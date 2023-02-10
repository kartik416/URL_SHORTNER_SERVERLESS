# URL_SHORTNER_SERVERLESS
Serverless implementation of url shortner using python and aws services.

App folder contains flask application which deals with the web application.

encoder.py contains code logic to create unique hashed value based on url.

lambda_function.py is code that is run in aws lambda compute service which handles request to create short url.

lambda_function_to_fetch contains logic to fetch long url from the database.

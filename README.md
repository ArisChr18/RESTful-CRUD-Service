# RESTful API service performing CRUD operations on Google's Firestore Cloud Database, developed in Python Flask

Used Python Flask framework to build a simple RESTful API service performing Create, Read, Update and Delete operations on a Google Firestore database. The project is deployed on Google Cloud Platform and connected to Firestore.

This application allows the user to read, add, update, or delete records on Firestore using GET/POST/PUT/DEL functions. The fields have to be in this specific format:
(username, email, password)

Used Postman to perform GET, POST, PUT and DELETE functions using JSON.
The application is served over https, and it can be accessed from this url : https://cc-coursework-346717.ew.r.appspot.com/accounts

How to deploy:
1. Create project in GCP
2. Create Dataset in Firestore
3. Name collection "Accounts"
4. Download files https://github.com/ArisChr18/RESTful-CRUD-Service.git
5. Download SDK SHELL
6. Run command (SDK SHELL):
     gcloud init
7. Create Service Account
8. Download JSON private key from created service account
9. Set GOOGLE_APPLICATION_CREDENTIALS environment variable in your machine as shown below:
     $env:GOOGLE_APPLICATION_CREDENTIALS="c:\gcpkeys\<filename>.json"
10. Command Prompt Commands:
     C:\CRUD-REST-SERVICE>gcloud init
     C:\CRUD-REST-SERVICE>gcloud app deploy
     C:\CRUD-REST-SERVICE>gcloud app browse (Add "/accounts" in url)
11. Download Postman https://www.postman.com/
12. Use Postman's workspace to perform GET/POST/PUT/DELETE operations (paste url and send requests)

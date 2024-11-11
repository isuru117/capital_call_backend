# Capital Call Backend API
The backend API for the Capital Call Application, providing a RESTful interface to manage Capital Call data efficiently.

## Demo
#### View a live demo of the API : [Capital Call API Demo](https://ccapi.isuruedirisinghe.com/)

All available endpoints are documented using Swagger API with OpenAPI 3.0 for easy reference and testing.
![Swagger API Documentation Screenshot](https://github.com/user-attachments/assets/acc66563-d23f-46c5-a78b-69d1080a824b)

## Requirements
To run this application, ensure you have the following:

- **Python**: Version 3.10 or later
- **Django**: Version 5.0 or later, with **Django REST Framework**: 3.15
- **Docker**: Version 3.8 or later
- **PostgreSQL**: Version 17.0 or later

## Setup
To get started, deploy the application using Docker Compose:
```bash
docker-compose up --build
```

### Key Features
- **Unit Testing**: Unit tests for the service layer.
- **Continuous Integration**: GitHub Actions for automated testing and build processes upon commit, ensuring continuous integration.
- **Automated Deployment**: Integrated deployment pipeline to Render host for seamless and automatic deployment on code changes.





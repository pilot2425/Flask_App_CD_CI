pipeline {
    agent {
        docker {
            image 'python:3.11-slim'
            args '-u root'
        }
    }

    environment {
        DOCKER_IMAGE = "flask-app"
        DOCKER_TAG = "main"
    }

    stages {
        stage('Clonar código') {
            steps {
                checkout scm
            }
        }

        stage('Instalar dependencias') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Linting (flake8)') {
            steps {
                sh 'flake8 app tests --count --show-source --statistics'
            }
        }

        stage('Ejecutar tests') {
            steps {
                sh 'coverage run -m pytest'
                sh 'coverage report -m'
            }
        }

        stage('Construir imagen Docker') {
            steps {
                sh 'docker build -t flask-app:main .'
            }
        }
    }
}

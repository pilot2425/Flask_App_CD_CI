pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "flask-app"
        DOCKER_TAG = "main"
        AWS_DEFAULT_REGION = 'eu-west-1'
    }

    stages {
        stage('Clonar código') {
            steps {
                checkout scm
            }
        }

        stage('Instalar dependencias y ejecutar tests') {
            agent {
                docker {
                    image 'python:3.11-slim'
                    args '-u root'
                }
            }
            steps {
                sh '''
                    pip install -r requirements.txt  // Instala todas las dependencias necesarias
                    flake8 app tests --count --show-source --statistics  // Linting
                    coverage run -m pytest  // Ejecutar tests
                    coverage report -m  // Mostrar reporte de coverage
                '''
            }
        }

        stage('Construir imagen Docker') {
            steps {
                sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
            }
        }

        stage('Subir imagen a DockerHub') {
            when {
                expression {
                    return env.DOCKER_TAG in ['develop', 'main', 'master']
                }
            }
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh """
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} $DOCKER_USER/${DOCKER_IMAGE}:${DOCKER_TAG}
                        docker push $DOCKER_USER/${DOCKER_IMAGE}:${DOCKER_TAG}
                    """
                }
            }
        }
    }
}

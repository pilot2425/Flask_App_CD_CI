pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "flask-app"
        DOCKER_TAG = "${env.BRANCH_NAME}"
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
                script {
                    docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                }
            }
        }

        stage('Push a Docker Hub') {
            when {
                branch 'main'
                or {
                    branch 'develop'
                    branch 'master'
                }
            }
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    sh "docker push ${DOCKER_IMAGE}:${DOCKER_TAG}"
                }
            }
        }
    }
}

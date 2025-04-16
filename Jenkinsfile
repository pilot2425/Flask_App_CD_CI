pipeline {
    agent any

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
            agent {
                docker {
                    image 'python:3.11-slim'
                    args '-u root'
                }
            }
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Linting (flake8)') {
            agent {
                docker {
                    image 'python:3.11-slim'
                    args '-u root'
                }
            }
            steps {
                sh 'pip install flake8'  // Instala flake8 si no viene en requirements.txt
                sh 'flake8 app tests --count --show-source --statistics'
            }
        }

        stage('Ejecutar tests') {
            agent {
                docker {
                    image 'python:3.11-slim'
                    args '-u root'
                }
            }
            steps {
                sh 'pip install -r requirements.txt'
                sh 'coverage run -m pytest'
                sh 'coverage report -m'
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
                    return env.DOCKER_TAG == 'develop' || env.DOCKER_TAG == 'main' || env.DOCKER_TAG == 'master'
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
        stage('Infraestructura como código - Terraform') {
            when {
                expression {
                    return env.DOCKER_TAG in ['main', 'master', 'develop']
                }
            }
            agent {
                docker {
                    image 'hashicorp/terraform:1.6' // Usa una imagen oficial de Terraform
                    args '-u root'
                }
            }
            environment {
                AWS_DEFAULT_REGION = 'eu-west-1'
            }
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws-creds',
                    accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                    secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
                ]]) {
                    sh '''
                        cd infra
                        terraform init
                        terraform workspace new $DOCKER_TAG || terraform workspace select $DOCKER_TAG
                        terraform apply -auto-approve -var="bucket_name=flask-app-jenkins-${DOCKER_TAG}"
                    '''
                }
            }
        }

    }
}

pipeline {
    agent any

    environment {
        IMAGE_NAME = 'xsstrike'
        IMAGE_TAG  = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Image') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -t ${IMAGE_NAME}:latest .'
            }
        }

        stage('Deploy & Run') {
            steps {
                sh 'docker run --rm ${IMAGE_NAME}:latest -u "https://public-firing-range.appspot.com/reflected/parameter/reflected_xss?q=hello" --skip'
            }
        }
    }

    post {
        success {
            echo 'Image built and container ran successfully.'
        }
        failure {
            echo 'Pipeline failed — check the stage logs above.'
        }
    }
}

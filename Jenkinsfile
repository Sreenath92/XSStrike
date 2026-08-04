pipeline {
    agent any

    parameters {
        string(
            name: 'SCAN_URL',
            defaultValue: 'https://public-firing-range.appspot.com/reflected/parameter/reflected_xss?q=hello',
            description: 'Target URL for XSStrike to scan'
        )
    }

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

        stage('Lint') {
            steps {
                sh 'docker run --rm --entrypoint sh ${IMAGE_NAME}:${IMAGE_TAG} -c "pip install --no-cache-dir flake8 -q && flake8 . --count --select=E901,E999,F821,F822,F823 --show-source --statistics"'
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKERHUB_USER', passwordVariable: 'DOCKERHUB_PASS')]) {
                    sh '''
                        echo "$DOCKERHUB_PASS" | docker login -u "$DOCKERHUB_USER" --password-stdin
                        docker tag ${IMAGE_NAME}:${IMAGE_TAG} $DOCKERHUB_USER/${IMAGE_NAME}:${IMAGE_TAG}
                        docker tag ${IMAGE_NAME}:${IMAGE_TAG} $DOCKERHUB_USER/${IMAGE_NAME}:latest
                        docker push $DOCKERHUB_USER/${IMAGE_NAME}:${IMAGE_TAG}
                        docker push $DOCKERHUB_USER/${IMAGE_NAME}:latest
                        docker logout
                    '''
                }
            }
        }

        stage('Deploy & Run') {
            steps {
                sh 'docker run --rm ${IMAGE_NAME}:latest -u "${SCAN_URL}" --skip'
            }
        }
    }

    post {
        success {
            echo 'Lint passed, image built, and container ran successfully.'
        }
        failure {
            echo 'Pipeline failed — check the stage logs above.'
        }
    }
}

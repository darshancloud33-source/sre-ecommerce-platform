pipeline {

    agent any

    environment {
        REGISTRY = "localhost:5001"
        CHECKOUT_IMAGE = "localhost:5001/checkout-service"
        PAYMENT_IMAGE = "localhost:5001/payment-service"
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Unit Tests') {
            steps {
                sh '''
                    cd checkout-service
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                    pytest
                '''

                sh '''
                    cd payment-service
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                    pytest
                '''
            }
        }

        stage('Build Docker Images') {
            steps {
                sh '''
                    docker build \
                    -t ${CHECKOUT_IMAGE}:${IMAGE_TAG} \
                    checkout-service
                '''

                sh '''
                    docker build \
                    -t ${PAYMENT_IMAGE}:${IMAGE_TAG} \
                    payment-service
                '''
            }
        }

        stage('Push Images') {
            steps {
                sh '''
                    docker push ${CHECKOUT_IMAGE}:${IMAGE_TAG}
                    docker push ${PAYMENT_IMAGE}:${IMAGE_TAG}
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    kubectl apply -f k8s/namespace.yaml
                    kubectl apply -f k8s/checkout-deployment.yaml
                    kubectl apply -f k8s/checkout-service.yaml
                    kubectl apply -f k8s/payment-deployment.yaml
                    kubectl apply -f k8s/payment-service.yaml
                '''
            }
        }
    }
}

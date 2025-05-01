pipeline {
    agent {
        docker {
            image 'python:3.12'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }
    
    environment {
        DOCKER_IMAGE = 'twitter-sentiment-analysis'
        DOCKER_TAG = "${env.BUILD_NUMBER}"
        PYTHON_ENV = "${WORKSPACE}\\.venv"
        STREAMLIT_PORT = '8502'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup Python Environment') {
            steps {
                sh '''
                    python --version
                    python -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    python -c "import nltk; nltk.download('stopwords')"
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    python -m pytest tests/ --cov=app.py --cov-report=term-missing
                '''
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    try {
                        sh 'docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .'
                    } catch (Exception e) {
                        error "Failed to build Docker image: ${e.message}"
                    }
                }
            }
        }
        
        stage('Push Docker Image') {
            steps {
                script {
                    try {
                        withDockerRegistry([credentialsId: 'docker-hub-credentials', url: '']) {
                            sh '''
                                docker push ${DOCKER_IMAGE}:${DOCKER_TAG}
                                docker push ${DOCKER_IMAGE}:latest
                            '''
                        }
                    } catch (Exception e) {
                        error "Failed to push Docker image: ${e.message}"
                    }
                }
            }
        }
        
        stage('Deploy') {
            steps {
                sh '''
                    if docker ps -q --filter "name=twitter-sentiment-analysis" | grep -q . ; then
                        docker stop twitter-sentiment-analysis
                        docker rm twitter-sentiment-analysis
                    fi
                    
                    docker run -d \
                        -p ${STREAMLIT_PORT}:${STREAMLIT_PORT} \
                        --name twitter-sentiment-analysis \
                        ${DOCKER_IMAGE}:${DOCKER_TAG}
                    
                    # Wait for container to be healthy
                    sleep 10
                    
                    # Verify container is running
                    if ! docker ps --filter "name=twitter-sentiment-analysis" --format "{{.Status}}" | grep -q "Up"; then
                        echo "Container failed to start"
                        exit 1
                    fi
                '''
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        success {
            echo 'Pipeline completed successfully!'
            echo "Application is running at http://localhost:${STREAMLIT_PORT}"
        }
        failure {
            echo 'Pipeline failed!'
            echo 'Check the logs for more details.'
        }
    }
} 
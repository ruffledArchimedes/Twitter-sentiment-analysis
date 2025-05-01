pipeline {
    agent any
    
    environment {
        PYTHON_ENV = "${WORKSPACE}/.venv"
        STREAMLIT_PORT = '8502'
    }
    
    stages {
        stage('Setup Python') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            python3 -m venv .venv
                            . .venv/bin/activate
                            python3 -m pip install --upgrade pip
                        '''
                    } else {
                        bat '''
                            python -m venv .venv
                            .venv\\Scripts\\activate.bat
                            python -m pip install --upgrade pip
                        '''
                    }
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            . .venv/bin/activate
                            pip install streamlit==1.31.1 nltk==3.8.1 scikit-learn==1.4.1.post1 pandas==2.2.1 numpy==1.26.4 pytest==8.0.2 pytest-cov==4.1.0
                            python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
                        '''
                    } else {
                        bat '''
                            .venv\\Scripts\\activate.bat
                            pip install streamlit==1.31.1 nltk==3.8.1 scikit-learn==1.4.1.post1 pandas==2.2.1 numpy==1.26.4 pytest==8.0.2 pytest-cov==4.1.0
                            python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
                        '''
                    }
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            . .venv/bin/activate
                            python -m pytest tests/ -v
                        '''
                    } else {
                        bat '''
                            .venv\\Scripts\\activate.bat
                            python -m pytest tests/ -v
                        '''
                    }
                }
            }
        }

        stage('Build Application') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            . .venv/bin/activate
                            streamlit run app.py --server.port=${STREAMLIT_PORT} &
                        '''
                    } else {
                        bat '''
                            .venv\\Scripts\\activate.bat
                            start /B streamlit run app.py --server.port=%STREAMLIT_PORT%
                        '''
                    }
                }
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
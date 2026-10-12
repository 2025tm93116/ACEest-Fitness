pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Build and Lint') {
            steps {
                sh 'python3 -m venv .venv'
                sh '.venv/bin/python -m pip install -r requirements.txt'
                sh '.venv/bin/python -m compileall -q app.py tests'
                sh '.venv/bin/ruff check app.py tests'
            }
        }
        stage('Pytest') {
            steps { sh '.venv/bin/python -m pytest -v' }
        }
        stage('Docker Build') {
            steps { sh 'docker build -t aceest-fitness:jenkins .' }
        }
    }
    post {
        always { echo 'ACEest Fitness validation pipeline finished.' }
    }
}

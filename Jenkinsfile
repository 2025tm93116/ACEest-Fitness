
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                sh '''
                    python3 -m venv .venv
                    .venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Syntax Check') {
            steps {
                sh '.venv/bin/python -m compileall -q app.py tests'
            }
        }

        stage('Lint') {
            steps {
                sh '.venv/bin/ruff check app.py tests'
            }
        }

        stage('Pytest') {
            steps {
                sh '.venv/bin/pytest -v'
            }
        }
    }
}


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
                sh '''
                    echo "Workspace: $WORKSPACE"
                    ls -la "$WORKSPACE"
                    export PYTHONPATH="$WORKSPACE"
                    .venv/bin/python -m pytest -v
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'SonarScanner'

                    withSonarQubeEnv('SonarQube') {
                        sh "${scannerHome}/bin/sonar-scanner"
                    }
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    script {
                        def qg = waitForQualityGate()

                        if (qg.status != 'OK') {
                            error "Quality Gate failed: ${qg.status}"
                        }
                    }
                }
            }
        }

        stage('Docker Build and Push') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKERHUB_USER',
                        passwordVariable: 'DOCKERHUB_TOKEN'
                    )
                ]) {
                    sh '''
                        set -eu

                        IMAGE_REPO="${DOCKERHUB_USER}/aceest-fitness"
                        IMAGE_TAG="1.0-${BUILD_NUMBER}"

                        echo "Building Docker image: ${IMAGE_REPO}:${IMAGE_TAG}"

                        echo "$DOCKERHUB_TOKEN" | docker login \
                            --username "$DOCKERHUB_USER" \
                            --password-stdin

                        trap 'docker logout >/dev/null 2>&1 || true' EXIT

                        docker build \
                            -t "${IMAGE_REPO}:${IMAGE_TAG}" \
                            -t "${IMAGE_REPO}:latest" \
                            .

                        docker push "${IMAGE_REPO}:${IMAGE_TAG}"
                        docker push "${IMAGE_REPO}:latest"

                        echo "Docker image published successfully."
                    '''
                }
            }
        }
    }
}

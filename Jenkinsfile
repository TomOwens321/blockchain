pipeline {
    agent { label 'ubuntu' }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Testing') {
            steps {
                sh 'scripts/run_tests.sh'
            }
        }
    }
}

pipeline {
    agent { label 'jslave' }
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

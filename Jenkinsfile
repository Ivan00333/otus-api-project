pipeline {
  agent {
    dockerfile {
      filename 'Dockerfile'
      additionalBuildArgs '--pull'
    }
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Run tests') {
      steps {
        sh 'pytest --clean-alluredir --alluredir=allure-results'
      }
    }
  }

  post {
    always {
      allure results: [[path: 'allure-results']], includeProperties: false
    }
  }
}

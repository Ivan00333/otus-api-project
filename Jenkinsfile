pipeline {
  agent any

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }
    stage('Setup Python') {
      steps {
        sh '''
          python3 -m venv .venv
          . .venv/bin/activate
          pip install -r requirements.txt
        '''
      }
    }
    stage('Run Tests') {
      steps {
        sh '''
          . .venv/bin/activate
          pytest --clean-alluredir --alluredir=allure-results
        '''
      }
    }
  }

  post {
    always {
      allure([
        includeProperties: false,
        jdk: '',
        results: [[path: 'allure-results']],
        reportBuildPolicy: 'ALWAYS'
      ])
    }
  }
}

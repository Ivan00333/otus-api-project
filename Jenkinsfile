pipeline {
  agent {
    docker {
      image 'python:3.13-slim'
      args  '--user root'
    }
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Install dependencies') {
      steps {
        sh '''
          python3 -m venv .venv
          . .venv/bin/activate
          pip install --upgrade pip
          pip install -r requirements.txt
        '''
      }
    }

    stage('Run tests') {
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
        results: [[path: 'allure-results']]
      ])
    }
  }
}

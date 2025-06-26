pipeline {
  agent any

  parameters {
    string(name: 'BRANCH', defaultValue: 'framework', description: 'Git branch to test')
    string(name: 'NUM_WORKERS', defaultValue: '1', description: 'Number of pytest-xdist workers')
  }

  environment {
        USERS_CLIENT__URL = 'https://reqres.in/api/'
    }

  stages {
    stage('Checkout') {
      steps {
        checkout([
          $class: 'GitSCM',
          branches: [[name: "*/${params.BRANCH}"]],
          userRemoteConfigs: [[
            url: 'https://github.com/Ivan00333/otus-api-project.git'
          ]]
        ])
      }
    }

    stage('Setup Virtualenv') {
            steps {
                sh '''
                  python3 -m venv .venv
                  . .venv/bin/activate
                  pip install --upgrade pip
                  pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                  . .venv/bin/activate
                  pytest -n ${NUM_WORKERS} --clean-alluredir --alluredir=allure-results
                '''
            }
        }
    }

  post {
    always {
      allure results: [[path: 'allure-results']], includeProperties: false
    }
  }
}

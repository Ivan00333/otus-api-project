pipeline {
  agent any

  // Параметризация ветки
  parameters {
    string(name: 'BRANCH', defaultValue: 'framework', description: 'Git branch to test')
  }

  stages {
    stage('Checkout') {
      steps {
        // Чекаут той ветки, что выбрал пользователь
        checkout([
          $class: 'GitSCM',
          branches: [[name: "*/${params.BRANCH}"]],
          userRemoteConfigs: [[
            url: 'git@github.com:your-org/your-repo.git',
            credentialsId: 'your-ssh-creds-id'
          ]]
        ])
      }
    }

    stage('Setup venv & Install') {
      steps {
        script {
          if (isUnix()) {
            sh '''
              python3 -m venv .venv
              . .venv/bin/activate
              pip install --upgrade pip
              pip install -r requirements.txt
            '''
          } else {
            bat '''
              python -m venv .venv
              .\\.venv\\Scripts\\Activate.ps1
              pip install --upgrade pip
              pip install -r requirements.txt
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
              pytest --clean-alluredir --alluredir=allure-results
            '''
          } else {
            bat '''
              .\\.venv\\Scripts\\Activate.ps1
              pytest --clean-alluredir --alluredir=allure-results
            '''
          }
        }
      }
    }
  }

  post {
    always {
      // Публикуем Allure-отчёт
      allure results: [[path: 'allure-results']], includeProperties: false
    }
  }
}

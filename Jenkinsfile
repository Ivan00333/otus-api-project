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
                  pytest --clean-alluredir --alluredir=allure-results
                '''
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

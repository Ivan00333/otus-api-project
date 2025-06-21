pipeline {
  agent any

  // 1) Параметризуем ветку
  parameters {
    string(
      name: 'BRANCH',
      defaultValue: 'framework',
      description: 'Git branch to checkout'
    )
  }

  stages {
    stage('Checkout') {
      steps {
        git url: 'https://github.com/Ivan00333/otus-api-project.git', branch: 'framework'
      }
    }

    stage('Build Docker Image') {
      steps {
        sh 'docker build -t tests .'
        sh 'docker version'
      }
    }

    stage('Run Tests') {
      steps {
        sh """
          . .venv/bin/activate
          pytest --clean-alluredir --alluredir=allure-results
        """
      }
    }
  }

  post {
    always {
      // 4) Публикация Allure-отчёта
      allure([
        includeProperties: false,
        results: [[path: 'allure-results']]
      ])
    }
  }
}

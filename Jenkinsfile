pipeline {
  agent any

  // 1) Параметризуем ветку
  parameters {
    string(
      name: 'BRANCH',
      defaultValue: 'main',
      description: 'Git branch to checkout'
    )
  }

  // 2) Указываем инструменты (если настроены в Global Tool Configuration)
  tools {
    python 'Python3'     // здесь имя вашей установки Python в Jenkins
  }

  stages {
    stage('Checkout') {
      steps {
        // 3) Чекаут нужной ветки
        checkout([
          $class: 'GitSCM',
          branches: [[name: "*/${params.BRANCH}"]],
          userRemoteConfigs: [[
            url: 'git@github.com:your-org/your-repo.git',
            credentialsId: 'your-git-credentials-id'
          ]]
        ])
      }
    }

    stage('Setup & Install') {
      steps {
        sh """
          python3 -m venv .venv
          . .venv/bin/activate
          pip install --upgrade pip
          pip install -r requirements.txt
        """
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

pipeline {
    /* Поднятие контейнера из вашего Dockerfile —
       здесь Jenkins сам соберёт образ перед запуском */
    agent {
        dockerfile {
            // Ваш Dockerfile лежит в корне проекта
            filename 'Dockerfile'
            // Запускать на любой ноде с Docker Engine

            // Всегда подтягивать свежий базовый образ
            additionalBuildArgs '--pull'
        }
    }

    options {
        // Вставлять таймстемпы в логи
        timestamps()
        // Пропускать оставшиеся стадии, если какая-то упала
        skipStagesAfterUnstable()
    }

    stages {
        stage('Checkout') {
          steps {
            git url: 'https://github.com/Ivan00333/otus-opencart-ui-testing.git', branch: 'jenkins'
          }
        }

        stage('Run tests') {
            steps {
                // Внутри контейнера уже установлен Python, Poetry и зависимости
                sh '''
                  # опционально: если хотите увидеть версию Poetry/Python
                  poetry --version
                  python --version

                  pytest --clean-alluredir --alluredir=allure-results
                '''
            }
        }
    }

    post {
        always {
            // Публикация результатов Allure
            allure([
                includeProperties: false,
                results: [[path: 'allure-results']]
            ])
        }
    }
}

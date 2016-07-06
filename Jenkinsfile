#!groovy

node {
    stage 'Test'

    git url: 'https://github.com/DatapuntAmsterdam/zwaailicht'

    sh 'docker-compose build'
    sh 'docker-compose run -u root web python manage.py jenkins'

    step([$class: 'JUnitResultArchiver', testResults: 'reports/junit.xml'])
}
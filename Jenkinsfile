#!groovy

node {
    stage 'Checkout'
        checkout scm

    stage 'Test'

        sh 'docker-compose build'
        sh 'docker-compose run -u root web python manage.py jenkins'

        step([$class: 'JUnitResultArchiver', testResults: 'reports/junit.xml'])

    
}
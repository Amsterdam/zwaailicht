#!groovy

node {

    IMAGE = "admin.datapunt.amsterdam.nl:5000/datapunt/zwaailicht"
    TAG = "${env.BRANCH}"

    stage "Checkout"
        checkout scm

    stage "Test"

        try {
            sh "docker-compose build"
            sh "docker-compose run --rm -u root web python manage.py jenkins"

            step([$class: "JUnitResultArchiver", testResults: "reports/junit.xml"])

        }
        finally {
            sh "docker-compose stop"
            sh "docker-compose rm -f"
        }


    stage "Build"

        sh "docker build -t ${IMAGE}:${TAG} --pull=true web"
        sh "docker push ${IMAGE}:${TAG}"

        if (TAG.equals("master")) {
            sh "docker tag ${IMAGE}:${TAG} ${IMAGE}:latest"
            sh "docker push ${IMAGE}:latest"
        }

}
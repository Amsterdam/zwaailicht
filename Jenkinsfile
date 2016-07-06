#!groovy

node {

    BRANCH = "${env.BRANCH}"

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

        image = docker.build("admin.datapunt.amsterdam.nl:5000/datapunt/zwaailicht:${BRANCH}", "web")
        image.push()

        if (BRANCH.equals("master")) {
            image.push("latest")
        }
}
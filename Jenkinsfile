#!groovy

String BRANCH = "${env.BRANCH_NAME}"
String INVENTORY = (BRANCH == "master" ? "production" : "acceptance")


def tryStep(String message, Closure block, Closure tearDown = null) {
    try {
        block();
    }
    catch (Throwable t) {
        slackSend message: "${env.JOB_NAME}: ${message} failure ${env.BUILD_URL}", channel: '#ci-channel', color: 'danger'

        warning(message)
        throw t;
    }
    finally {
        if (tearDown) {
            tearDown();
        }
    }
}


def warning(String msg) {
    slackSend message: "${JOB_NAME}: $msg ${env.BUILD_URL}", channel: '#ci-channel', color: 'danger'
}

node {

    stage "Checkout"
        checkout scm

    stage "Test"

        tryStep "build", {
            sh "docker-compose build"
        }

        tryStep "test", {
            sh "docker-compose run --rm -u root web python manage.py jenkins"
        }, {
            step([$class: "JUnitResultArchiver", testResults: "reports/junit.xml"])

            sh "docker-compose stop"
            sh "docker-compose rm -f"
        }

    stage "Build"

        try {
            def image = docker.build("admin.datapunt.amsterdam.nl:5000/datapunt/zwaailicht:${BRANCH}", "web")
            image.push()

            if (BRANCH == "master") {
                image.push("latest")
            }
        }
        catch (err) {
            warning 'build failure'
            throw err
        }

    stage "Deploy"

        try {
            build job: 'Subtask_Openstack_Playbook',
                    parameters: [
                            [$class: 'StringParameterValue', name: 'INVENTORY', value: INVENTORY],
                            [$class: 'StringParameterValue', name: 'PLAYBOOK', value: 'deploy-zwaailicht.yml'],
                            [$class: 'StringParameterValue', name: 'BRANCH', value: BRANCH],
                    ]
        }
        catch (err) {
            warning 'deployment failure'
            throw err
        }
}
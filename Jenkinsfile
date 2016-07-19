#!groovy

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

        tryStep "build", {
            def image = docker.build("admin.datapunt.amsterdam.nl:5000/datapunt/zwaailicht:${BRANCH}", "web")
            image.push()
        }

    stage "Deploy to ACC"

        tryStep "deployment", {
            build job: 'Subtask_Openstack_Playbook',
                    parameters: [
                            [$class: 'StringParameterValue', name: 'INVENTORY', value: 'acceptance'],
                            [$class: 'StringParameterValue', name: 'PLAYBOOK', value: 'deploy-zwaailicht.yml'],
                            [$class: 'StringParameterValue', name: 'BRANCH', value: 'master'],
                    ]
        }

    stage "Wait for approval"

        input "Deploy ${env.JOB_NAME} to Production?"

    stage "Deploy to PROD"

        tryStep "image tagging", {
            image.push("master")
            image.push("latest")
        }

        tryStep "deployment", {
            build job: 'Subtask_Openstack_Playbook',
                    parameters: [
                            [$class: 'StringParameterValue', name: 'INVENTORY', value: 'production'],
                            [$class: 'StringParameterValue', name: 'PLAYBOOK', value: 'deploy-zwaailicht.yml'],
                            [$class: 'StringParameterValue', name: 'BRANCH', value: 'master'],
                    ]
        }

}
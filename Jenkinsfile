#!groovy

String BRANCH = "${env.BRANCH_NAME}"
String INVENTORY = (BRANCH == "master" ? "production" : "acceptance")

def warning(msg) {
    slackSend message: "${JOB_NAME}: $msg ${env.BUILD_URL}", channel: '#ci-channel', color: 'danger'
}

node {

    stage "Checkout"
        checkout scm

    stage "Test"
        try {
            sh "docker-compose build"
        }
        catch (err) {
            warning 'build failure'
            throw err
        }


        try {
            sh "docker-compose run --rm -u root web python manage.py jenkins"
        }
        catch (err) {
            warning 'test failures'
            throw err
        }
        finally {
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
                            [$class: 'StringParameterValue', name: 'PLAYBOOK', value: 'deploy-zwaailicht-123.yml'],
                            [$class: 'StringParameterValue', name: 'BRANCH', value: BRANCH],
                    ]
        }
        catch (err) {
            warning 'deployment failure'
            throw err
        }
}
#!groovy

String BRANCH = "${env.BRANCH_NAME}"
String INVENTORY = (BRANCH == "master" ? "production" : "acceptance")

def warning(msg) {
    slackSend message: "$msg ${env.BUILD_URL}", channel: '#ci-channel', color: 'danger'
}

node {

    stage "Checkout"
        checkout scm

    stage "Test"
        try {
            sh "docker-compose build"
        }
        catch (err) {
            warning 'Zwaailicht service: build failure'
            throw err
        }


        try {
            sh "docker-compose run --rm -u root web python manage.py jenkins"
        }
        catch (err) {
            warning 'Zwaailicht service: test failures'
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
            warning 'Zwaailicht service: build failure'
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
            warning 'Zwaailicht service: deployment failure'
            throw err
        }
}
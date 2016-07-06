#!groovy

node {

    String BRANCH = "${env.BRANCH_NAME}"
    String INVENTORY = (BRANCH == "master" ? "production" : "acceptance")

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

        def image = docker.build("admin.datapunt.amsterdam.nl:5000/datapunt/zwaailicht:${BRANCH}", "web")
        image.push()

        if (BRANCH == "master") {
            image.push("latest")
        }

    stage "Deploy"

        build job: 'Subtask_Openstack_Playbook',
                parameters: [
                        [$class: 'StringParameterValue', name: 'INVENTORY', value: INVENTORY],
                        [$class: 'StringParameterValue', name: 'PLAYBOOK', value: 'deploy-zwaailicht.yml'],
                        [$class: 'StringParameterValue', name: 'BRANCH', value: BRANCH],
                ]
}
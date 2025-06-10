pipeline{
    agent { label 'aws-slave' }
    environment{
        DOCKER_CREDENTIALS = credentials('docker_hub')
        DOCKER_REPO = credentials('docker_repo')
        DEPLOY_IP = credentials('ec2_address')
        ERROR_MSG = "General error happend, look for ${env.BUILD_ID} logs for additional information"
    }

    options{ skipDefaultCheckout() }

    stages {
        stage ('clean'){
            steps{
                cleanWs()
            }
        }
        stage ('checkout'){
            steps{
                checkout scm
            }
        }

        stage ('build') {
            steps {
                echo "start build stage.."
                sh 'docker compose up --build -d'
                sh 'sleep 10'
                script {
                    def serviceHealthy = false
                    def exit_code = sh(
                    script: "curl localhost:5000",
                    returnStatus: true)
                        
                    if (exit_code == 0){
                        env.SERVICE_HEALTH = 'healthy'
                        serviceHealthy = true
                    }

                    echo "exit code is: ${exit_code}"

                    if (!serviceHealthy) {
                        env.ERROR_MSG = "${env.BUILD_ID}: Failed to load flask app"
                        error("Service Unhealthy")
                    }
                }
            }
        }

        stage ('set tags'){
            steps{
                script {
                    def shortCommit = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
                    def time_now = sh(script: "date +%Y%m%d_%H%M%S", returnStdout: true).trim()
                    env.IMAGE_TAGGED_SHA = "${DOCKER_REPO}/lambda_automations:${shortCommit}"
                    env.IMAGE_TAGGED_TIME = "${DOCKER_REPO}/lambda_automations:${time_now}"
                }
            }
        }

        stage ('publish for debug'){
            steps {
                sh "docker login -u ${DOCKER_CREDENTIALS_USR} -p ${DOCKER_CREDENTIALS_PSW}" 
                sh "docker tag lambda_automations ${env.IMAGE_TAGGED_SHA}"
                sh "docker push ${env.IMAGE_TAGGED_SHA}"
            }
        }
        

        stage('tests and sca in parallel') {
            parallel {
                stage('integration tests') {
                    steps {
                        script {
                            echo "start integration tests.."
                            def status = sh (
                                script: 'docker compose -f tests/pytest/compose.yaml run tests',
                                returnStatus: true
                            )
                            if (status != 0) {
                                env.ERROR_MSG = "Tests Failed, Look for: ${env.BUILD_ID} logs for additional information"
                                error("${env.BUILD_ID} Tests Failed")
                            }
                        }
                    }
                }

                stage('sca scan') {
                    steps {
                        script {
                            echo "start sca scan on image: ${env.IMAGE_TAGGED_SHA}"
                            def scaStatus = sh (
                                script: """
                                export DOCKER_IMAGE=${env.IMAGE_TAGGED_SHA}
                                docker compose -f tests/trivy/compose.yaml run trivy
                                """,
                                returnStatus: true
                            )
                            if (scaStatus != 0) {
                                env.ERROR_MSG = "sca scan failed on image: ${env.IMAGE_TAGGED_SHA}"
                                error("sca vulnerabilities found")
                            }
                        }
                    }
                }
            }
        }



        stage ('re-tag after tests'){
            steps{
                    sh "docker tag ${env.IMAGE_TAGGED_SHA} ${env.IMAGE_TAGGED_TIME}"
                    sh "docker push ${env.IMAGE_TAGGED_TIME}"
            }
        }

        stage ('continuous deployment') {
            steps {
                sshagent(['deploy_app']) {
                    script {
                        sh """ssh  -o StrictHostKeyChecking=no ec2-user@"${DEPLOY_IP}" \\
                        "docker login -u ${DOCKER_CREDENTIALS_USR} -p ${DOCKER_CREDENTIALS_PSW} && \\
                        export DOCKER_IMAGE=${env.IMAGE_TAGGED_TIME} && \\
                        docker compose up --build -d && \\
                        docker system prune -a"
                        """
                    }
                }
            }
        }
    }


    post {
        failure {
            script {
                slackSend(channel: "#devops-alerts", color: "red", message: env.ERROR_MSG)
            }
        }
        success {
            slackSend(channel: "#succeeded", color: "green", message: "Build ${env.BUILD_ID} succeeded, merged open by: ${gitlabUserName}")
            acceptGitLabMR(useMRDescription: true, removeSourceBranch: false)
        }
    }
}

pipeline {
  agent any
  stages {
    stage('build') {
      steps {
        echo "This is Build stage"
        cd src/pycrudapi
        docker build --rm -t pycrudapi .
      }
    }
    stage('test') {
      steps {
        echo "This is test stage"
      }
    }
    stage('deploy') {
      steps {
        echo "THis is deploy stage"
      }
    }
  }
}

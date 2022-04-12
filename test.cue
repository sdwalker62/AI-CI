package aiml_ci

import (
    "dagger.io/dagger"
    // "dagger.io/dagger/core"
    // "universe.dagger.io/bash"
    "universe.dagger.io/docker"
)

#BuildTestImage: docker.#Dockerfile & {
    dockerfile: contents: """
        FROM python:3.9
        COPY . .
        RUN pip install -r requirements.txt
        CMD sh run_tests.sh
        """
}


dagger.#Plan & {
    client: {
        filesystem: "./src": read: contents: dagger.#FS
        network: "unix:///var/run/docker.sock": connect: dagger.#Socket
    }

    actions: test: {
        build: #BuildTestImage & {
            source: client.filesystem."./src".read.contents
        }
        exec_tests: docker.#Run & {
            input: build.output
            mounts: docker: {
                dest:     "."
                contents: client.network."unix:///var/run/docker.sock".connect
            }
        }
    }
}

package forge

import (
    "dagger.io/dagger"
    // "dagger.io/dagger/core"
    // "universe.dagger.io/bash"
    "universe.dagger.io/docker"
)

dagger.#Plan & {
    client: filesystem: "./test_app": read: contents: dagger.#FS

    actions: {
        test: {
            build: docker.#Build & {
                steps: [
                    docker.#Pull & {
                        source: "python:3.9"
                    },
                    docker.#Copy & {
                        contents: client.filesystem."./test_app".read.contents
                        dest: "/"
                    },            
                    docker.#Set & {
                        config: cmd: ["python", "/unit_tests/unit_tests.py"]
                    }
                ]
            }
            run: docker.#Run & {
                input: build.output
                command: {
                    name: "python"
                    args: ["/unit_tests/unit_tests.py"]
                }
            }
        }
    }
}

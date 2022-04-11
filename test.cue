package forge

import (
    "dagger.io/dagger"
    "dagger.io/dagger/core"
    // "universe.dagger.io/bash"
    "universe.dagger.io/docker"
)

// Write a greeting to a file, and add it to a directory
#AddHello: {
    // The input directory
    dir: dagger.#FS

    // The name of the person to greet
    name: string | *"world"

    write: core.#WriteFile & {
        input: dir
        path: "hello-\(name).txt"
        contents: "hello, \(name)!"
    }

    // The directory with greeting message added
    result: write.output
}

#CoverageReport: {
    // The input directory
    dir: dagger.#FS

    // The name of the person to greet
    name: string | *"world"

    write: core.#WriteFile & {
        input: dir
        path: "hello-\(name).txt"
        contents: "hello, \(name)!"
    }

    copy: core.#Copy & {
        input: dir
        source: "hello-\(name).txt"
        destination: "thiswascopied.txt"
    }

    result: copy.output
}

dagger.#Plan & {
    // client: filesystem: ".": read: contents: dagger.#FS

    actions: {
        hello: #AddHello & {
            dir: client.filesystem.".".read.contents
        },
        stuff: #CoverageReport & {
            dir: client.filesystem.".".read.contents
        }
        test: {
            build: docker.#Build & {
                steps: [
                    docker.#Pull & {
                        source: "python:3.9"
                    },
                    docker.#Copy & {
                        contents: client.filesystem."./src".read.contents
                        dest: "/"
                    },
                    docker.#Run & {
                        command: {
                            name: "pip"
                            args: ["install", "coverage"]
                        }
                    }         
                    // docker.#Set & {
                    //     config: cmd: ["python", "/unit_tests/unit_tests.py"]
                    // }
                ]
            }
            run: { 
                docker.#Run & {
                    input: build.output
                    command: {
                        name: "sh"
                        args: ["run_tests.sh"]
                    }
                }
            }
        }
    }
    client: filesystem: ".": {
        read: contents: dagger.#FS
        write: contents: actions.stuff.result
    }
}

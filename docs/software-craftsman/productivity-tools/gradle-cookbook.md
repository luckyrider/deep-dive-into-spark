# Gradle Cookbook

## Overview
Gradle的文档非常好，要入门直接看官方文档即可。

* http://www.gradle.org/docs/current/userguide/userguide.html

### features
* A very flexible general purpose build tool like Ant
* Ant tasks and builds as first class citizens
* Gradle's build scripts are written in Groovy, not XML.
* The Gradle Wrapper allows you to execute Gradle builds on machines where Gradle is not installed.
* Very powerful dependency management (based on Apache Ivy)
* Full support for your existing Maven or Ivy repository infrastructure.

### Why Groovy?

* Although Gradle is a general purpose build tool at its core, its main focus are Java projects.

## Up and Running
download:

    wget http://services.gradle.org/distributions/gradle-1.11-bin.zip

unpack:

    unzip gradle-1.11-bin.zip

config:

    add GRADLE_HOME/bin to your PATH environment variable

running:

    gradle -v

## Configuration
JVM options for running Gradle can be set via environment variables. You can use GRADLE_OPTS or JAVA_OPTS. Those variables can be used together. JAVA_OPTS is by convention an environment variable shared by many Java applications. A typical use case would be to set the HTTP proxy in JAVA_OPTS and the memory options in GRADLE_OPTS. Those variables can also be set at the beginning of the gradle or gradlew script. 

### Proxy Settings:

modify gradle.properties:

```
systemProp.http.proxyHost=<server>
systemProp.http.proxyPort=<port>

systemProp.https.proxyHost=<server>
systemProp.https.proxyPort=<port>
```

## Fundamentals

Everything in Gradle sits on top of two basic concepts: projects and tasks.

Every Gradle build is made up of one or more projects. a project might represent a library JAR or a web application. It might represent a distribution ZIP assembled from the JARs produced by other projects. A project does not necessarily represent a thing to be built. It might represent a thing to be done, such as deploying your application to staging or production environments.

Each project is made up of one or more tasks. A task represents some atomic piece of work which a build performs. This might be compiling some classes, creating a JAR, generating javadoc, or publishing some archives to a repository.

The gradle command looks for a file called build.gradle in the current directory.

A plugin is an extension to Gradle which configures your project in some way, typically by adding some pre-configured tasks which together do something useful. One such plugin is the Java plugin. This plugin adds some tasks to your project which will compile and unit test your Java source code, and bundle it into a JAR file. 

references:

* http://www.gradle.org/docs/current/userguide/tutorial_using_tasks.html

## Build lifecycle
A Gradle build has three distinct phases.

* Initialization
* Configuration
* Execution

* http://www.gradle.org/docs/current/userguide/build_lifecycle.html

### 重要文件
build.gradle。类似于maven的pom.xml，以下所有的配置都是在这个文件中。
setting.gradle:类似于maven中setting.xml，不过setting.gradle可以放在项目中，优先加载项目中的setting.gradle。

## Java Plugin
### use java plugin
build.gradle:

	apply plugin: 'java'

Gradle expects to find your production source code under src/main/java and your test source code under src/test/java. In addition, any files under src/main/resources will be included in the JAR file as resources, and any files under src/test/resources will be included in the classpath used to run the tests. All output files are created under the build directory, with the JAR file ending up in the build/libs directory.

### build
```
> gradle build
:compileJava
:processResources
:classes
:jar
:assemble
:compileTestJava
:processTestResources
:testClasses
:test
:check
:build
```

to skip test:

* gradle build -x test, or
* gradle assemble

see discussion: http://stackoverflow.com/questions/4597850/gradle-build-without-tests

### Creating an Eclipse project
```
apply plugin: 'eclipse'
gradle eclipse
```

### Idea

```
gradle idea
gradle cleanIdea idea
```

see more at: [Gradle中使用idea插件的一些实践](http://www.geekcome.com/content-10-2336-1.html)

### Multi-project Java build
settings.gradle

    include "shared", "api", "services:webservice", "services:shared"

we will define this common configuration in the root project, using a technique called configuration injection. Here, the root project is like a container and the subprojects method iterates over the elements of this container - the projects in this instance - and injects the specified configuration. This way we can easily define the manifest content for all archives, and some common dependencies

## Dependency management
dependency management is made up of two pieces:

* dependencies
* publications

In Gradle dependencies are grouped into configurations. A configuration is simply a named set of dependencies. We will refer to them as dependency configurations. 

下载的包会放在 $HOME/.gradle/cache/ 目录下，基本跟maven一样。

### external dependencies
There is a shortcut form for declaring external dependencies, which uses a string of the form "group:name:version". 

```
dependencies {
    compile group: 'org.hibernate', name: 'hibernate-core', version: '3.6.7.Final'
}

dependencies {
    compile 'org.hibernate:hibernate-core:3.6.7.Final'
}
```

### repositories
Gradle looks for them in a repository. A repository is really just a collection of files, organized by group, name and version. Gradle understands several different repository formats, such as Maven and Ivy, and several different ways of accessing the repository, such as using the local file system or HTTP. 

```
repositories {
    mavenCentral()
}

repositories {
    maven {
        url "http://repo.mycompany.com/maven2"
    }
}

repositories {
    ivy {
        url "http://repo.mycompany.com/repo"
    }
}
```

You can also have repositories on the local file system. This works for both Maven and Ivy repositories.

```
repositories {
    ivy {
        // URL can refer to a local directory
        url "../local-repo"
    }
}
```

### Publishing artifacts

references:

* http://www.gradle.org/docs/current/userguide/artifact_dependencies_tutorial.html

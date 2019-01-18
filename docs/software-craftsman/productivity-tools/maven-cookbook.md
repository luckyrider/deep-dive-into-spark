# Maven Cookbook

## Outline
* maven fundamentals
* install and config
* most used plugins
* troubleshooting

## Maven Fundamentals

### What is Maven
Maven is essentially a project management and comprehension tool to help with managing:

* builds
* documentation
* reporting
* dependencies
* SCMs
* releases
* distribution

Maven vs Ant:

* Ant is a build tool; Maven is a build system.

### Build Lifecycle
* three built-in lifecycles: default, clean, deploy
* A Build Lifecycle is Made Up of Phases
* A Build Phase is Made Up of Plugin Goals
* change phase-goal bindings through: packaging, plugin settings

see also:

* http://maven.apache.org/guides/index.html
* http://maven.apache.org/guides/introduction/introduction-to-the-lifecycle.html

### Plugins
Plugins are artifacts that provide goals to Maven. A plugin may have one or more goals. If you want to customize the build for a Maven project, this is done by adding or reconfiguring plugins. All plugins in Maven 2.0 look much like a dependency. A plugin will be automatically downloaded and used.

### Standard Directory Layout


### Dependency Management
Dependency scope:
* compile: default scope
* provided: like compile, but expect that jdk or container provide the dependency at runtime
* runtime: not required for compilation, but is for execution
* test

### Repositories
A repository in Maven is used to hold build artifacts and dependencies of varying types. There are strictly only two types of repositories: local and remote.

### Build Profiles
Build profiles are used to address portability.

### POM
Project Object Model

### archetype

```
mvn archetype:generate -DgroupId=com.vip -DartifactId=weiwo -DarchetypeArtifactId=maven-archetype-quickstart -DinteractiveMode=false
```

## Install and config

### Proxy
Modify: `${user.home}/.m2/settings.xml` or `/usr/local/maven/conf/settings.xml`

```
<settings>
  <proxies>
   <proxy>
      <active>true</active>
      <protocol>http</protocol>
      <host>proxy.somewhere.com</host>
      <port>8080</port>
      <username>proxyuser</username>
      <password>somepassword</password>
      <nonProxyHosts>www.google.com|*.somewhere.com</nonProxyHosts>
    </proxy>
  </proxies>
</settings>
```

```
export MAVEN_OPTS="-DsocksProxyHost=127.0.0.1 -DsocksProxyPort=1080"

export MAVEN_OPTS="-Dhttp.proxyHost=xxx -Dhttp.proxyPort=80 -Dhttps.proxyHost=xxx -Dhttps.proxyPort=80"
```

## Most used Plugins

### maven-assembly-plugin
The Assembly Plugin for Maven is primarily intended to allow users to aggregate the project output along with its dependencies, modules, site documentation, and other files into a single distributable archive.

The main goal in the assembly plugin is the single goal. It is used to create all assemblies. All other goals are deprecated and will be removed in a future release.

Configuration options:

* prefabricated assembly descriptors, you configure which descriptor to use with the <descriptorRefs>/<descriptorRef> parameter.
* custom assembly descriptor called src.xml in the src/main/assembly directory

Execution: `assembly:single`

References:

* http://maven.apache.org/plugins/maven-assembly-plugin/usage.html

### maven-shade-plugin

> Exception in thread "main" java.lang.SecurityException: Invalid signature file digest for Manifest main attributes

For those who got this error when trying to create an uber-jar with maven-shade-plugin, the solution is to exclude manifest signature files by adding the following lines to the plugin configuration:

```
<configuration>
    <filters>
        <filter>
            <artifact>*:*</artifact>
            <excludes>
                <exclude>META-INF/*.SF</exclude>
                <exclude>META-INF/*.DSA</exclude>
                <exclude>META-INF/*.RSA</exclude>
            </excludes>
        </filter>
    </filters>
    <!-- Additional configuration. -->
</configuration>
```

### maven-compiler-plugin
generatedSourcesDirectory = ${project.build.directory}/generated-sources/annotations

see also:

* http://maven.apache.org/plugins/maven-compiler-plugin/compile-mojo.html
* http://stackoverflow.com/questions/19633505/maven-generated-sources-not-compiled

### avro-maven-plugin

outputDirectory = ${project.build.directory}/generated-sources/avro

see:

* http://grepalex.com/2013/05/24/avro-maven/

### Maven Dependency Plugin
Get dependency:
```
mvn dependency:get -Dartifact=groupId:artifactId:version[:packaging][:classifier]
```

Get sources and Javadocs
```
mvn dependency:sources
mvn dependency:resolve -Dclassifier=javadoc
```
see more: http://tedwise.com/2010/01/27/maven-micro-tip-get-sources-and-javadocs/

### maven release plugin
http://maven.apache.org/maven-release/maven-release-plugin/

## Trouble Shooting

### local repository缓存问题
Problem: 明明~/.m2/repository里面有对应的库，build时却说找不着

Solution: 可能是缓存问题，对应的库删掉，重新下载可能就解决了。

### 国内镜像
国内OSChina提供的镜像，非常不错

```
<mirror>
      <id>CN</id>
      <name>OSChina Central</name>
      <url>http://maven.oschina.net/content/groups/public/</url>
      <mirrorOf>external:*</mirrorOf>
    </mirror>
```

通过设置`external:*`，使得不会再去访问super POM里的其他repository，而只使用OSChina，提高速度。

see more:

* http://blog.sina.com.cn/s/blog_5ff02a9f0101ojh3.html
* http://my.oschina.net/sunchp/blog/100634

由于网络问题，有时候从oschina下载POM或者JAR文件是损坏的，会导致build失败。

> [ERROR] Failed to execute goal org.apache.maven.plugins:maven-site-plugin:3.4:attach-descriptor (attach-descriptor) on project hadoop-main: Execution attach-descriptor of goal org.apache.maven.plugins:maven-site-plugin:3.4:attach-descriptor failed: A required class was missing while executing org.apache.maven.plugins:maven-site-plugin:3.4:attach-descriptor: org/codehaus/plexus/util/xml/XmlStreamReader

maven-site-plugin所依赖的`org.codehaus:plexus-utils`不正确。可能有2类错误：

* invalid POM

```
[WARNING] The POM for org.apache.maven:maven-artifact-manager:jar:2.2.0 is invalid, transitive dependencies (if any) will not be available, enable debug logging for more details
```

* Checksum validation failed for JAR file

```
WARNING] Checksum validation failed, expected <html> but is 66a644c26e8a1cd2945981422c33ba247226a2ef for http://maven.oschina.net/content/groups/public/org/codehaus/plexus/plexus-interpolation/1.1/plexus-interpolation-1.1.jar
```

解决办法很简单，就是重新下载。

### _maven.repositories/_remote.repositories
两个文件类似，都是用来记录artifact来源的。

_maven.repositories

```
#NOTE: This is an internal implementation file, its format can be changed without prior notice.
#Fri Dec 11 08:43:53 CST 2015
commons-lang-2.6.pom>central=
```

_remote.repositories

```
#NOTE: This is an Aether internal implementation file, its format can be changed without prior notice.
#Mon Dec 14 22:44:14 CST 2015
apache-3.pom>CN=
```

with Maven 3.0.x, when an artifact is downloaded from a repository, maven leaves a _maven.repositories file to record where the file was resolved from. If you are building a project and the effective list of repositories does not include the location that the artifact was resolved from, then Maven decides that it is as if the artifact was not in the cache, and will seek to re-resolve the artifact…

I also had to remove _remote.repositories in the same way as the _maven.repositories described above. I'm using Maven 3.1.1

```
find ~/.m2/repository -name _remote.repositories -exec rm -v {} \;
find ~/.m2/repository -name _maven.repositories -exec rm -v {} \;
```

如果_maven.repositories/_remote.repositories存在，则在切换mirror之后，会重新下载artifact。为了避免这个问题，需要删除这两个文件。

相关issue:

* https://issues.apache.org/jira/browse/MNG-5185

### 注意事项
maven的repository并没有优先级的配置，也不能单独为某些依赖配置repository。所以如果项目配置了多个repository，在首次编绎时，会依次尝试下载依赖。如果没有找到，尝试下一个，整个流程会很长。所以尽量多个依赖放同一个仓库，不要每个项目都有一个自己的仓库。

see more: http://blog.csdn.net/hengyunabc/article/details/47308913

有个小技巧：如果某个依赖只在某个库里，可以修改`conf/settings.xml`只使用该库，以避免不断尝试多个库。



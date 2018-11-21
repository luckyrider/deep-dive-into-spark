package ddis.simpleapp

import org.apache.spark.launcher.SparkLauncher
import java.io.File

/**
  * appResource must be absolute path. A relative path is actually relative to
  * System.getProperty("user.dir"), which is /path/to/deep-dive-into-spark when run from IDEA.
  */
object SimpleAppRawChildProcessLauncher {
  def main(args: Array[String]): Unit = {
    val process = new SparkLauncher()
      .setAppResource(
        new File("examples/simpleapp/target/simpleapp-0.1.0.jar").getCanonicalPath)
      .setMainClass("ddis.simpleapp.SimpleApp")
      .setAppName("ddis.simpleapp.SimpleApp (raw child process)")
      .setMaster("yarn")
      .setConf(SparkLauncher.DRIVER_MEMORY, "512m")
      .launch();
    process.waitFor()
  }
}


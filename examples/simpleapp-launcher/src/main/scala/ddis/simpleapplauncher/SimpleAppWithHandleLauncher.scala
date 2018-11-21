package ddis.simpleapplauncher

import java.io.File

import org.apache.spark.launcher.SparkLauncher

/**
  * appResource must be absolute path. A relative path is actually relative to
  * System.getProperty("user.dir"), which is /path/to/deep-dive-into-spark when run from IDEA.
  */
object SimpleAppWithHandleLauncher {
  def main(args: Array[String]): Unit = {
    val handle = new SparkLauncher()
      .setAppResource(
        new File("examples/simpleapp/target/simpleapp-0.1.0.jar").getCanonicalPath)
      .setMainClass("ddis.simpleapp.SimpleApp")
      .setAppName("ddis.simpleapp.SimpleApp (with handle)")
      .setMaster("yarn")
      .setConf(SparkLauncher.DRIVER_MEMORY, "512m")
      .startApplication();
    Thread.sleep(60 * 1000)
  }
}


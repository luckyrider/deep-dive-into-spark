package ddis.sparkapps

import org.apache.spark.sql.SparkSession

object LineCounter {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder().getOrCreate()
    println("Num lines: " + countLines(spark, args(0)))
  }

  def countLines(spark: SparkSession, path: String): Long = {
    spark.read.textFile(path).count()
  }
}

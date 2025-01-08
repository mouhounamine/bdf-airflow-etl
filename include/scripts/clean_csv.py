from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, lower, to_date, year
from pyspark.sql.types import DoubleType

def main():
    spark = SparkSession \
        .builder \
        .appName("PySparkCleaning") \
        .enableHiveSupport() \
        .getOrCreate()

    # 1. Lecture du CSV brut
    csv_path = "./include/vgchartz-2024.csv"
    df_raw = (
        spark.read.format("csv")
        .option("header", "true")
        .option("inferSchema", "true")
        .option("escape", "\"")
        .option("multiLine", "true")
        .load(csv_path)
    )

    # 2. Nettoyage
    # 2.1 Supprimer les lignes dont certaines colonnes sont nulles
    df_cleaned = df_raw.dropna(
        subset=["title", "total_sales", "release_date", "console", "genre"]
    )

    # 2.2 Combler les valeurs nulles sur les ventes
    df_cleaned = df_cleaned.fillna({
        "na_sales": 0,
        "jp_sales": 0,
        "pal_sales": 0,
        "other_sales": 0
    })

    # 2.3 Convertir release_date au bon format date (si nécessaire)
    df_cleaned = df_cleaned.withColumn(
        "release_date",
        to_date(col("release_date"), "yyyy-MM-dd")
    )

    # 2.4 Uniformiser la casse pour console et genre
    df_cleaned = df_cleaned.withColumn("console", trim(lower(col("console"))))
    df_cleaned = df_cleaned.withColumn("genre", trim(lower(col("genre"))))

    # 2.5 Extraire l'année
    df_cleaned = df_cleaned.withColumn("release_year", year(col("release_date")))

    # 2.6 Forcer le type double
    sales_columns = ["total_sales", "na_sales", "jp_sales", "pal_sales", "other_sales"]
    for c in sales_columns:
        df_cleaned = df_cleaned.withColumn(c, col(c).cast(DoubleType()))

    # 3. Écriture dans Hive ou Parquet (partitionné par année par exemple)
    df_cleaned.write \
              .mode("overwrite") \
              .format("parquet") \
              .partitionBy("release_year") \
              .saveAsTable("db_videogames.clean_vg_sales")

    # 4. Fin de session
    spark.stop()

if __name__ == "__main__":
    main()
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, expr, sum as sum_, year
)

def main():
    # 1. Création de la session Spark
    spark = SparkSession.builder \
        .appName("VideoGameSalesAnalysis") \
        .getOrCreate()

    # 2. Chargement du fichier CSV local
    csv_path = "backend/airflow/data/raw/vgchartz-2024.csv"
    df = spark.read.csv(csv_path, header=True, inferSchema=True)

    # 3. Aperçu des données
    df.show(5)
    df.printSchema()

    # 4. Remplir les valeurs manquantes pour les colonnes de ventes
    df = df.na.fill(0, subset=["total_sales", "na_sales", "jp_sales", "pal_sales", "other_sales"])

    # --- ANALYSES ---

    # 4.1 Quel jeu a réalisé le plus de ventes au niveau mondial ?
    print("Jeu avec le plus de ventes globales :")
    df.orderBy(col("total_sales").desc()) \
      .select("title", "total_sales") \
      .limit(1) \
      .show()

    # 4.2 Extraire l'année à partir de la date de sortie et déterminer l'année où les ventes totales sont les plus élevées
    df = df.withColumn("year", year(col("release_date")))

    # Année ayant généré le plus de ventes
    print("Année avec le plus de ventes totales :")
    df.groupBy("year") \
      .agg(sum_("total_sales").alias("total_sales")) \
      .orderBy(col("total_sales").desc()) \
      .show(1)

    # 4.3 Ventes totales par année (pour voir l'évolution au fil des ans)
    print("Ventes totales par année :")
    df.groupBy("year") \
      .agg(sum_("total_sales").alias("total_sales")) \
      .orderBy("year") \
      .show()

    # 4.4 Nombre de jeux par console et genre
    print("Nombre de jeux par console et genre :")
    df.groupBy("console", "genre") \
      .count() \
      .orderBy(col("count").desc()) \
      .show()

    # 4.5 Quels jeux sont populaires dans une région mais sont des échecs dans d'autres régions ?
    df_regions = df.select("title", "na_sales", "jp_sales", "pal_sales", "other_sales") \
        .withColumn("max_region", expr("""
            CASE
                WHEN na_sales >= jp_sales AND na_sales >= pal_sales AND na_sales >= other_sales THEN 'NA'
                WHEN jp_sales >= na_sales AND jp_sales >= pal_sales AND jp_sales >= other_sales THEN 'JP'
                WHEN pal_sales >= na_sales AND pal_sales >= jp_sales AND pal_sales >= other_sales THEN 'PAL'
                ELSE 'Other'
            END
        """)) \
        .withColumn("min_region", expr("""
            CASE
                WHEN na_sales <= jp_sales AND na_sales <= pal_sales AND na_sales <= other_sales THEN 'NA'
                WHEN jp_sales <= na_sales AND jp_sales <= pal_sales AND jp_sales <= other_sales THEN 'JP'
                WHEN pal_sales <= na_sales AND pal_sales <= jp_sales AND pal_sales <= other_sales THEN 'PAL'
                ELSE 'Other'
            END
        """))

    # Jeux où la région la plus forte n'est pas la même que la plus faible
    print("Jeux populaires dans une région mais échecs dans une autre :")
    df_regions.filter(col("max_region") != col("min_region")) \
              .select("title", "max_region", "min_region") \
              .show()

    # 4.6 Top 10 des jeux les plus vendus en Amérique du Nord
    print("Top 10 des jeux (NA) :")
    df.orderBy(col("na_sales").desc()) \
      .select("title", "na_sales") \
      .limit(10) \
      .show()

    # 4.7 Top 10 des jeux les plus vendus au Japon
    print("Top 10 des jeux (Japon) :")
    df.orderBy(col("jp_sales").desc()) \
      .select("title", "jp_sales") \
      .limit(10) \
      .show()

    # 4.8 Top 10 des jeux les plus vendus en Europe/Afrique (PAL)
    print("Top 10 des jeux (PAL) :")
    df.orderBy(col("pal_sales").desc()) \
      .select("title", "pal_sales") \
      .limit(10) \
      .show()

    # 4.9 Top 10 des jeux les plus vendus dans le reste du monde
    print("Top 10 des jeux (Autres régions) :")
    df.orderBy(col("other_sales").desc()) \
      .select("title", "other_sales") \
      .limit(10) \
      .show()

    # 5. Vérification de la présence de valeurs nulles après le remplissage
    print("Check des valeurs nulles :")
    df.select([col(column).isNull().alias(column) for column in df.columns]).show()

    # 6. Arrêt de la session Spark
    spark.stop()


if __name__ == "__main__":
    main()

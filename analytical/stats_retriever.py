# analytics/stats_retriever.py

import pandas as pd


class StatsRetriever:
    """
    Step 3: Structured statistics layer.
    This class exposes business facts in a retrievable format.
    """

    def __init__(self, analyzer):
        self.analyzer = analyzer

    def get_global_metrics(self) -> dict:
        metrics = self.analyzer.basic_metrics()
        return {
            "total_sales": metrics["Total Sales"],
            "average_sales": metrics["Average Sales"],
            "median_sales": metrics["Median Sales"],
            "std_dev_sales": metrics["Sales Std Dev"]
        }

    def get_sales_by_region(self) -> pd.DataFrame:
        return self.analyzer.sales_by_region()

    def get_sales_by_product(self) -> pd.DataFrame:
        return self.analyzer.sales_by_product()

    def get_sales_over_time(self) -> pd.DataFrame:
        return self.analyzer.sales_over_time()

    def get_sales_by_year(self) -> pd.DataFrame:
        return self.analyzer.sales_by_year()

    def as_dict(self) -> dict:
        """
        Unified retrieval payload (LLM-ready).
        """
        return {
            "global_metrics": self.get_global_metrics(),
            "sales_by_region": self.get_sales_by_region().to_dict(),
            "sales_by_product": self.get_sales_by_product().to_dict(),
            "sales_over_time": self.get_sales_over_time().to_dict(),
            "sales_by_year": self.get_sales_by_year().to_dict(),
        }

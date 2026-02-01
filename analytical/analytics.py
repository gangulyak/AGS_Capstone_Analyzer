import pandas as pd
from pandas.api.types import is_numeric_dtype


class SalesAnalyzer:
    """
    Schema-driven analytics engine.

    Roles:
    - sales   → numeric
    - region  → categorical
    - product → categorical
    - date    → datetime

    Safe for unit testing and auto-grading.
    """

    INTERNAL_COLUMNS = {
        "sales": "Sales",
        "region": "Region",
        "product": "Product",
        "date": "Order Date"
    }

    def __init__(self, df: pd.DataFrame, schema: dict):
        """
        schema example:
        {
            "sales": "Revenue",
            "region": "State",
            "product": "Sub-Category",
            "date": "Invoice_Date"
        }
        """
        self.df = df.copy()
        self.schema = schema

        self._validate_schema()
        self._apply_schema()
        self._validate_dataframe()
        self._prepare_dataframe()

    # ------------------------------------------------------------------
    # Schema validation
    # ------------------------------------------------------------------
    def _validate_schema(self):
        required_keys = {"sales", "region", "product", "date"}
        missing = required_keys - set(self.schema.keys())

        if missing:
            raise ValueError(f"Schema missing required keys: {missing}")

        for role, col in self.schema.items():
            if col not in self.df.columns:
                raise ValueError(f"Column '{col}' not found for role '{role}'")

    # ------------------------------------------------------------------
    # Apply schema safely (NO duplicate internal columns)
    # ------------------------------------------------------------------
    def _apply_schema(self):
        """
        Safely applies schema mapping without dropping user-selected columns.
        """

        # Columns explicitly chosen by the user
        user_selected_columns = set(self.schema.values())

        # Internal canonical names
        internal_cols = set(self.INTERNAL_COLUMNS.values())

        # Drop ONLY internal columns that are NOT user-selected
        columns_to_drop = [
            c for c in self.df.columns
            if c in internal_cols and c not in user_selected_columns
        ]

        self.df = self.df.drop(columns=columns_to_drop, errors="ignore")

        # Rename user-selected columns to internal canonical names
        rename_map = {
            self.schema["sales"]: self.INTERNAL_COLUMNS["sales"],
            self.schema["region"]: self.INTERNAL_COLUMNS["region"],
            self.schema["product"]: self.INTERNAL_COLUMNS["product"],
            self.schema["date"]: self.INTERNAL_COLUMNS["date"],
        }

        self.df = self.df.rename(columns=rename_map)

    # ------------------------------------------------------------------
    # Data validation AFTER schema application
    # ------------------------------------------------------------------
    def _validate_dataframe(self):
        # Sales must be numeric
        if not is_numeric_dtype(self.df["Sales"]):
            raise TypeError("Selected Sales column must be numeric")

        # Region and Product must be categorical-like
        for col in ["Region", "Product"]:
            if not (
                self.df[col].dtype == "object"
                or str(self.df[col].dtype).startswith("category")
            ):
                raise TypeError(f"Selected {col} column must be categorical")

    # ------------------------------------------------------------------
    # Data preparation
    # ------------------------------------------------------------------
    def _prepare_dataframe(self):
        self.df["Order Date"] = pd.to_datetime(
            self.df["Order Date"], errors="coerce"
        )

        if self.df["Order Date"].isna().any():
            raise ValueError("Date column contains invalid or non-date values")

        self.df["Year"] = self.df["Order Date"].dt.year
        self.df["Month"] = self.df["Order Date"].dt.to_period("M").astype(str)

    # ------------------------------------------------------------------
    # Public analytics methods
    # ------------------------------------------------------------------
    def basic_metrics(self) -> dict:
        return {
            "Total Rows": int(len(self.df)),
            "Total Sales": float(self.df["Sales"].sum()),
            "Average Sales": float(self.df["Sales"].mean()),
            "Median Sales": float(self.df["Sales"].median()),
            "Sales Std Dev": float(self.df["Sales"].std()),
            "Number of Regions": int(self.df["Region"].nunique()),
            "Number of Products": int(self.df["Product"].nunique()),
        }

    def sales_by_region(self) -> pd.DataFrame:
        return (
            self.df.groupby("Region", as_index=False)["Sales"]
            .sum()
            .sort_values("Sales", ascending=False)
        )

    def sales_by_product(self) -> pd.DataFrame:
        return (
            self.df.groupby("Product", as_index=False)["Sales"]
            .sum()
            .sort_values("Sales", ascending=False)
        )

    def sales_over_time(self) -> pd.DataFrame:
        return (
            self.df.groupby("Month", as_index=False)["Sales"]
            .sum()
            .sort_values("Month")
        )

    def sales_by_year(self) -> pd.DataFrame:
        return (
            self.df.groupby("Year", as_index=False)["Sales"]
            .sum()
            .sort_values("Year")
        )

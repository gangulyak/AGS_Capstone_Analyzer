# analytical/visualizer.py

from typing import Optional
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import seaborn as sns
import pandas as pd

# ------------------------------------------------------------------
# Global seaborn theme (SET ONCE)
# ------------------------------------------------------------------
sns.set_theme(
    style="whitegrid",
    palette="colorblind",
    context="talk"
)

# ------------------------------------------------------------------
# Axis formatter for large numbers
# ------------------------------------------------------------------
def human_readable(x, pos):
    if abs(x) >= 1_000_000:
        return f"{x/1_000_000:.1f}M"
    elif abs(x) >= 1_000:
        return f"{x/1_000:.0f}K"
    else:
        return f"{int(x)}"


class SalesVisualizer:
    """
    Human-facing visualization layer.
    Returns matplotlib Figure objects.
    """

    @staticmethod
    def plot_sales_dashboard(
        sales_over_time: pd.DataFrame,
        sales_by_year: pd.DataFrame,
        sales_by_product: pd.DataFrame,
        sales_by_region: pd.DataFrame,
        currency: Optional[str] = None,
    ):
        fig, axes = plt.subplots(2, 2, figsize=(16, 10))

        y_label = "Sales" if not currency else f"Sales ({currency})"

        # --------------------------------------------------
        # 1. Monthly sales (current year)
        # --------------------------------------------------
        if not sales_over_time.empty:
            current_year = pd.to_datetime(
                sales_over_time["Month"]
            ).dt.year.max()

            monthly_current_year = sales_over_time[
                pd.to_datetime(sales_over_time["Month"]).dt.year == current_year
            ]

            sns.lineplot(
                data=monthly_current_year,
                x="Month",
                y="Sales",
                marker="o",
                linewidth=2.5,
                ax=axes[0, 0],
            )
            axes[0, 0].set_title(f"Monthly Sales – {current_year}")
            axes[0, 0].set_ylabel(y_label)
            axes[0, 0].tick_params(axis="x", rotation=45)
            axes[0, 0].yaxis.set_major_formatter(FuncFormatter(human_readable))

        # --------------------------------------------------
        # 2. Sales by year (last 4 years)
        # --------------------------------------------------
        if not sales_by_year.empty:
            last_years = sales_by_year.sort_values("Year").tail(4)

            sns.barplot(
                data=last_years,
                x="Year",
                y="Sales",
                hue="Year",
                legend=False,
                ax=axes[0, 1],
            )
            axes[0, 1].set_title("Sales by Year (Last 4 Years)")
            axes[0, 1].set_ylabel(y_label)
            axes[0, 1].yaxis.set_major_formatter(FuncFormatter(human_readable))

        # --------------------------------------------------
        # 3. Sales by product
        # --------------------------------------------------
        if not sales_by_product.empty:
            sns.barplot(
                data=sales_by_product,
                x="Sales",
                y="Product",
                hue="Product",
                legend=False,
                ax=axes[1, 0],
            )
            axes[1, 0].set_title("Sales by Product / Service")
            axes[1, 0].set_xlabel(y_label)
            axes[1, 0].xaxis.set_major_formatter(FuncFormatter(human_readable))

        # --------------------------------------------------
        # 4. Sales by region
        # --------------------------------------------------
        if not sales_by_region.empty:
            sns.barplot(
                data=sales_by_region,
                x="Sales",
                y="Region",
                hue="Region",
                legend=False,
                ax=axes[1, 1],
            )
            axes[1, 1].set_title("Sales by Region")
            axes[1, 1].set_xlabel(y_label)
            axes[1, 1].xaxis.set_major_formatter(FuncFormatter(human_readable))

        plt.tight_layout()
        return fig






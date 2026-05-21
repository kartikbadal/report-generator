import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import logging
import os

logger = logging.getLogger(__name__)

# Apply a clean global style to all charts

sns.set_theme(style = "whitegrid")

def save_bar_chart(df:pd.DataFrame,x_col: str, y_col: str, output_path : str) -> str:
    """
    Creates a bar chart and saves it to the output folder
    
    Args: 
        df: Input DataFrame
        x_col : Column to use on x-axis (categories e.g. Product)
        y_col : Column to use on y-axis(values e.g. Sales)
    
    Returns:
        output_path : Path where the charts were saved

    """

    try:
        # Create a figure with axis object
        fig, ax = plt.subplots(figsize = (10,5))
        
        # Draw a bar chart on the axis
        sns.barplot(data= df, x= x_col, y =y_col, ax= ax)

        # Set title and axis labels

        ax.set_title(f"{y_col} by {x_col}", fontsize = 14)
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)

        # fix spacing so labels are not cut off
        plt.tight_layout()

        # Save chart
        plt.savefig(output_path)
        plt.close(fig)

        logger.info(f"Bar chart saved:{output_path}")
        return output_path
    
    except Exception as e:
        logger.error(f"Failed to create bar chart:{e}")
        raise

def save_line_chart(df: pd.DataFrame, x_col: str, y_col : str, output_path :str) -> str:
    """
    Creates a line chart and save it to the output folder.
    Best used for showing trends over time

    Args:
        df : Input Dataframe
        x_col : Column to use on x-axis (e.g. Date, Month)
        y_col : Column to use on y-axis (e.g. Revenue)
        output_path : Full file path where chart will be saved
    
    Returns:
        output_path : Path where the chart will be saved.
    """
    try:
        fig, ax = plt.subplots(figsize = (10,5))
        sns.lineplot(data = df, x= x_col, y= y_col, ax= ax)
        ax.set_title(f"{y_col} trend over {x_col}", fontsize = 14)
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)

        plt.tight_layout()
        plt.savefig(output_path)
        plt.close(fig)

        logger.info(f"Line chart saved : {output_path}")
        return output_path
    
    except Exception as e:
        logger.error(f"Failed to create line chart :{e}")
        raise


def save_correlation_heatmap(df: pd.DataFrame, output_path: str) -> str:
    """
    Creates a corelation heatmap for all numeric columns.
    Shows how strongly each numeric column relates to others.

    Args: 
        df: Input DataFrame
        output_path : Full file path where chart will be saved

    Returns: 
        output_path : Full file where chart will be saved
    """

    try:
        # Select only numeric columns - strings cannot be corelated
        numeric_df = df.select_dtypes(include= "number")

        if numeric_df.empty:
            raise ValueError("No numeric columns found for heatmap.")
        
        fig, ax = plt.subplots(figsize = (10,6))

        # annot = True shows corelation value inside each celll
        # fmt = ".2f" rounds value to 2 decimal places
        # cmap = "coolwarm" - blue for negative, red for positive corelation

        sns.heatmap(
            numeric_df.corr(),
            annot=True,
            fmt = ".2f",
            cmap= "coolwarm",
            ax=ax
        )

        ax.set_title("Corelation Heatmap", fontsize = 14)

        plt.tight_layout()
        plt.savefig(output_path)
        plt.close(fig)

        logger.info(f"Heatmap saved:{output_path}")
        return output_path
    
    except Exception as e:
        logger.error(f"Failed to create heatmap:{e}")
        raise

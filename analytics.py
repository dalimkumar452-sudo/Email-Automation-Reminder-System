"""
Email Automation System - Data Analytics & Visualization Module
Author: Dalim Kumar
Description: Reads the delivery report CSV and generates 5 professional charts
             (Pie, Bar, Line, Donut, and Tally Table). Automatically saves
             them to the 'images/outputs' directory.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configuration for Output Directory
OUTPUT_DIR = "images/outputs"
REPORT_CSV = "outputs/delivery_report.csv"

def setup_environment():
    """Creates the output directories if they do not exist."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    # Set a professional plotting style
    sns.set_theme(style="whitegrid", palette="pastel")

def load_data():
    """Loads the delivery report from CSV."""
    if not os.path.exists(REPORT_CSV):
        print(f"❌ Error: {REPORT_CSV} not found. Please run main.py first to generate data.")
        return None
    
    df = pd.read_csv(REPORT_CSV)
    if df.empty:
        print("❌ Error: The CSV report is empty. No data to visualize.")
        return None
        
    # Convert Timestamp column to actual datetime objects
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    return df

def generate_pie_chart(df):
    """Generates a Pie Chart showing the success vs failure ratio."""
    status_counts = df['Status'].value_counts()
    
    plt.figure(figsize=(8, 6))
    colors = ['#4CAF50', '#F44336'] if 'Sent' in status_counts.index else sns.color_palette("pastel")
    
    plt.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', 
            startangle=140, colors=colors, wedgeprops={'edgecolor': 'white'})
    
    plt.title('Email Delivery Status Ratio', fontsize=16, fontweight='bold')
    
    filepath = os.path.join(OUTPUT_DIR, "01_status_pie_chart.png")
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Saved: {filepath}")

def generate_bar_chart(df):
    """Generates a Bar Chart showing count of emails sent per user."""
    plt.figure(figsize=(10, 6))
    
    user_counts = df['Name'].value_counts()
    sns.barplot(x=user_counts.index, y=user_counts.values, palette="Blues_d")
    
    plt.title('Total Emails Processed per Contact', fontsize=16, fontweight='bold')
    plt.xlabel('Contact Name', fontsize=12)
    plt.ylabel('Number of Emails', fontsize=12)
    plt.xticks(rotation=45)
    
    filepath = os.path.join(OUTPUT_DIR, "02_user_bar_chart.png")
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Saved: {filepath}")

def generate_donut_chart(df):
    """Generates a professional Donut Chart for overall system performance."""
    status_counts = df['Status'].value_counts()
    
    plt.figure(figsize=(8, 6))
    colors = ['#2196F3', '#FF9800']
    
    # Create a pie chart, then add a white circle in the middle to make it a donut
    plt.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', 
            startangle=90, colors=colors, pctdistance=0.85)
    
    centre_circle = plt.Circle((0,0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    
    plt.title('System Performance Overview', fontsize=16, fontweight='bold')
    
    filepath = os.path.join(OUTPUT_DIR, "03_performance_donut_chart.png")
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Saved: {filepath}")

def generate_tally_table(df):
    """Generates a static visual Data Table (Tally) of the summary."""
    summary_df = df.groupby(['Name', 'Status']).size().reset_index(name='Total Count')
    
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.axis('tight')
    ax.axis('off')
    
    # Create the table
    table = ax.table(cellText=summary_df.values, colLabels=summary_df.columns, 
                     cellLoc='center', loc='center')
    
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.2, 1.5)
    
    plt.title('Email Delivery Tally Matrix', fontsize=16, fontweight='bold', pad=20)
    
    filepath = os.path.join(OUTPUT_DIR, "04_summary_tally_table.png")
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Saved: {filepath}")

def generate_line_trend(df):
    """Generates a Line Graph to show email volume over time."""
    # Extract just the date for grouping
    df['Date'] = df['Timestamp'].dt.date
    trend_df = df.groupby('Date').size().reset_index(name='Emails Sent')
    
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=trend_df, x='Date', y='Emails Sent', marker='o', color='purple', linewidth=2.5)
    
    plt.title('Email Dispatch Trend Over Time', fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Volume', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    
    filepath = os.path.join(OUTPUT_DIR, "05_dispatch_trend_line.png")
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Saved: {filepath}")

def run_analytics():
    """Main function to execute the analytics workflow."""
    print("\n📊 Starting Data Visualization Engine...")
    setup_environment()
    
    df = load_data()
    if df is not None:
        generate_pie_chart(df)
        generate_bar_chart(df)
        generate_donut_chart(df)
        generate_tally_table(df)
        generate_line_trend(df)
        print("\n🎉 All professional visualizations have been saved in 'images/outputs/'\n")

if __name__ == "__main__":
    run_analytics()
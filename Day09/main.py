import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
from datetime import datetime

DEADLINES = {
    'day01': datetime(2025, 11, 2, 22, 0), 'day02': datetime(2025, 11, 9, 22, 0),
    'day03': datetime(2025, 11, 16, 22, 0), 'day04': datetime(2025, 11, 23, 22, 0),
    'day05': datetime(2025, 11, 29, 22, 0), 'day06': datetime(2025, 12, 6, 22, 0),
    'day08': datetime(2025, 12, 30, 22, 0), 'day09': datetime(2026, 1, 10, 22, 0),
    'proposal': datetime(2026, 1, 11, 22, 0)
}


def load_and_process(file_path):
    rows = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                p = line.strip().split('\t')
                if len(p) < 4: continue
                raw_sub = p[2]
                day_match = re.search(r'day\s?(\d+)', raw_sub, re.I)
                subj = f"day{day_match.group(1).zfill(2)}" if day_match else (
                    'proposal' if 'proposal' in raw_sub.lower() else 'other')
                name = re.split(r'\s+by\s+', raw_sub, flags=re.I)[-1].strip() if ' by ' in raw_sub.lower() else \
                raw_sub.split()[-1]
                ts = datetime.fromisoformat(p[-1].replace('Z', '+00:00')).replace(tzinfo=None)
                deadline = DEADLINES.get(subj)
                diff = (deadline - ts).total_seconds() / 3600 if deadline else 0

                rows.append({
                    'Name': name, 'Subj': subj, 'Time': ts,
                    'Hour': ts.hour, 'Day': ts.strftime('%A'),
                    'LeadTime': diff, 'IsLate': ts > deadline if deadline else False
                })
        return pd.DataFrame(rows)
    except Exception as e:
        print(f"Error: {e}")
        return pd.DataFrame()

def create_master_table(df):
    print("\n" + "=" * 95)
    print(f"{'GENERAL STUDENT PERFORMANCE TABLE':^95}")
    print("=" * 95)

    avg_lead = df.groupby('Subj')['LeadTime'].transform('mean')
    df['Pace'] = df['LeadTime'] - avg_lead

    master = df.groupby('Name').agg(
        Total_Tasks=('Subj', 'nunique'),
        Lates=('IsLate', 'sum'),
        Avg_Lead_Hrs=('LeadTime', 'mean'),
        Peer_Pace_Score=('Pace', 'mean')
    )
    master['Reliability'] = (master['Total_Tasks'] - (master['Lates'] * 0.5)).round(2)
    master = master.sort_values('Reliability', ascending=False)
    print(master.to_string(formatters={
        'Avg_Lead_Hrs': '{:,.1f}h'.format,
        'Peer_Pace_Score': '{:+.1f}h'.format
    }))
    print("=" * 95)
    return master


def plot_dashboard(df):
    if df.empty: return
    plt.style.use('seaborn-v0_8-muted')
    fig, axes = plt.subplots(3, 2, figsize=(18, 18))  

    sns.kdeplot(data=df, x='LeadTime', fill=True, ax=axes[0, 0], color='orange')
    axes[0, 0].axvline(0, color='red', lw=2, linestyle='--')
    axes[0, 0].set_title("1. Deadline Distribution (How early/late?)", fontsize=14)

    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    heat = df.groupby(['Day', 'Hour']).size().unstack(fill_value=0).reindex(day_order)
    sns.heatmap(heat, cmap="YlGnBu", ax=axes[0, 1], annot=True, cbar=False)
    axes[0, 1].set_title("2. Peak Activity Hot Zones", fontsize=14)

    df_sorted = df.sort_values(['Name', 'Time'])
    df_sorted['Gap'] = df_sorted.groupby('Name')['Time'].diff().dt.total_seconds() / 3600
    sns.boxplot(x='Subj', y='Gap', data=df_sorted[df_sorted['Gap'] < 1000], ax=axes[1, 0])
    axes[1, 0].set_title("3. Task Complexity (Hours between submissions)", fontsize=14)
    axes[1, 0].set_yscale('log')

    df['Subj'].value_counts().sort_index().plot(kind='bar', ax=axes[1, 1], color='teal')
    axes[1, 1].set_title("4. Student Retention", fontsize=14)

    late_counts = df.groupby(['Subj', 'IsLate']).size().unstack(fill_value=0)
    late_counts.plot(kind='bar', stacked=True, ax=axes[2, 0], color=['#55a868', '#c44e52'])
    axes[2, 0].set_title("5. Punctuality Per Assignment", fontsize=14)
    axes[2, 0].legend(["On-Time", "Late"])

    avg_lead = df.groupby('Subj')['LeadTime'].transform('mean')
    df['Pace'] = df['LeadTime'] - avg_lead
    df.groupby('Name')['Pace'].mean().nlargest(10).plot(kind='barh', ax=axes[2, 1], color='#8172b3')
    axes[2, 1].set_title("6. Top 10 'Proactive' Students (Relative to Peer Avg)", fontsize=14)

    plt.tight_layout()
    plt.show()


# --- EXECUTION ---
df = load_and_process('subjects.txt')
if not df.empty:
    master_stats = create_master_table(df)

    plot_dashboard(df)

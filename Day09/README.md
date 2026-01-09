# Code Overview

This code parses raw submission data from `subjects.txt` to analyze student behavior, participation trends, and possible assignment complexity.

---

## Scoring Methodology

The analysis uses **three primary custom metrics** to evaluate student engagement:

### 1. Reliability Score ("The Consistency Index")

**Formula:**  
```math
Score = (Total\ Unique\ Assignments) - 0.5 \times Late\ Submissions
```
This metric penalizes late submissions and thus measures approximately how "reliable" a student is.

---

### 2. Peer Pace Score (Proactivity)


**Formula:**  

```math
Peer\ Pace\ Score = Individual\ Lead\ Time - Class\ Average\ Lead\ Time
```
This metric compares students to the average submission time of the class and scores the student based on the gap between the student's submission time and the class's average submission time. 
This metric is measured per assignment, so for example:
- If the class average for *Day 08* is submitting **2 hours before** the deadline, and a student submits **12 hours before**, they receive a **+10.0h Peer Pace Score**.

---

### 3. Task Complexity ("Gap" Analysis)

This metric measures the **time elapsed between two consecutive submissions by the same student**.

If the average gap between *Day 05 → Day 06* is **2 days**, but the gap for *Day 08* is **6 days**, we can mathematically demonstrate that **Day 08 is a significantly more difficult or complex task**.

---

## Visual Dashboard Breakdown

The program generates a **6-figure dashboard** providing a 360° view of the course:

### Dashboard Components

- **Deadline Distribution (KDE)**  
  A density plot showing the *"Submission Wave"*. Visualizes whether the class is:
  - "Living on the edge" (peaking at the deadline)
  - Working comfortably ahead of time

- **Activity Heatmap**  
  Cross-references **Day of Week × Hour of Day** to identify student activity *"Hot Zones"*.  

- **Complexity Boxplot**  
  Uses a **logarithmic scale** to show the distribution of time gaps between assignments.

- **Retention Funnel**  
  A bar chart showing the number of students per assignment.  

- **Punctuality per Assignment**  
  A stacked bar chart (**On-Time vs. Late**) revealing whether certain deadlines were too strict or unclear.

- **Proactivity Leaderboard**  
  Highlights the **Top 10 students** who consistently outperform the class average.

---

## Technical Implementation

- **Python 3.10+**
- **Pandas**
- **Matplotlib & Seaborn** 
- **Regex (`re`)** 

---

## How to Run

1. Ensure `subjects.txt` is located in the **root directory**
2. Install dependencies:
   ```bash
   pip install pandas matplotlib seaborn
   ```
3. Execute the script:
   ```bash
   python main.py
   ```

---

## Output

- Ranked student performance table
- Engagement and punctuality metrics
- A comprehensive multi-figure visual dashboard

Designed for educators who want **data-driven insight**, not just grades.


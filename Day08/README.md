# Online Gaming Behavior Analysis

This folder contains a data analysis of player behaviors, demographics, and engagement metrics using a dataset of over 40,000 gamers taken from [Kaggle](https://www.kaggle.com/datasets/wasiqaliyasir/online-gaming-behavior-insight?resource=download). 
The code leverages **NumPy** for statistical computing, **Pandas** for data orchestration, **Folium** for geographic visualization, and **Matplotlib** for general visualization.

## Code Overview
The goal of this analysis is to uncover patterns in how different demographics interact with games. Moving beyond simple counts to look at "Intensity," conversion rates, and geographic trends.

## File Structure
* `Gaming_behavior.ipynb`: The primary notebook containing all logic and visualizations.
* `online_gaming_behavior_insights.csv`: The raw dataset containing player IDs, age, gender, location, genre, playtime, and engagement levels.
* `README.md`: Project documentation.

## Requirements
To run this code, ensure you have the following Python libraries installed:
```bash
pip install pandas numpy matplotlib folium
```


#  Key Analysis & Insights

### 1. Geographic Player Mapping
The global distribution of the player base is visualized using **Folium**. 
* **The 'Other' Category:** Players from undefined locations are mapped to the South Atlantic Ocean. This approach was taken to ensure visibility is maintained for all data points without regional skewing.


### 2. Playtime Metrics
Rather than relying on standard Pandas grouping, **NumPy array masking** is utilized to calculate the average `PlayTimeHours` per region. 

### 3. Gender & Game Difficulty
The relationship between **Gender** and **GameDifficulty** is examined. 
* **Context:** Acknowledgement is given to the sociological background of sexism within the gaming community's history. **Normalized Percentages** are applied so that difficulty preferences between male and female players can be compared fairly.
* **Sources**:
* [Sexism in Video Games and in the Gaming Community](https://www.researchgate.net/publication/345054712_Sexism_in_Video_Games_and_the_Gaming_Community)
* [Insights into Sexism](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0131613) - one of the most cited articles regarding women in eSports.
* [The Women Gamers Study of 2024](https://www.bryter-global.com/blog/female-gamers-survey-2024)
* [Hate is No Game](https://boundlessisrael.org/paper/285/file/307)

### 4. Age Demographics
The age distribution of the community is analyzed using binned histograms.
* **Statistical Overlays:** NumPy-calculated **Mean** and **Median** lines are included within the histogram to provide immediate context regarding the "typical" player age.

### 5. The "Intensity Score" vs. Purchases
A custom **Intensity Score** was developed to define player dedication:

$$\text{Intensity} = (0.6 \times \text{Scaled PlayTime}) + (0.4 \times \text{Scaled Session Frequency})$$

Through this metric, **"Grinder"** genres (characterized by high intensity and low spend) are compared against **"Whale"** genres (characterized by lower intensity and higher spend).

---

## How to Use

1. **The repository should be cloned** or the files downloaded.
2. **The file `online_gaming_behavior_insights.csv` must be placed** in the same directory as the notebook.
3. **`Gaming_behavior.ipynb` should be opened** in a Jupyter environment (such as VS Code or JupyterLab).
4. **All cells are to be run** to generate the interactive map and behavioral charts.

---
## AI usage:
### AI Used:
Gemini

### Prompt:
- Given this data, provide a code that can visualize the geographic distribution of the players on a world map.

---

title: DataCleanRL Environment Server
emoji: 🧹
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
app_port: 8000
base_path: /web
tags:

* openenv

---

# 🧹 DataCleanRL — Data Cleaning RL Environment

## 📌 Overview

DataCleanRL is an OpenEnv-based reinforcement learning environment where an AI agent cleans a messy dataset step by step.

The dataset contains:

* Missing values
* Outliers
* Duplicate rows

The agent must apply cleaning actions efficiently to maximize its score.

---

## 🚀 Key Features

### 🔹 Dynamic Dataset

Each reset generates a completely new dataset with random noise.
This prevents memorization and ensures generalization.

---

### 🔹 Action Space

* `fill_missing(column)`
* `remove_outliers(column)`
* `drop_duplicates`
* `do_nothing`

---

### 🔹 Reward System

* +0.30 → successful cleaning
* +0.20 → duplicates removed
* -0.10 → no effect
* -0.15 → invalid action
* -0.01 × step_count → efficiency penalty

---

### 🔹 Multi-Level Tasks

#### Task 1 — Fix Missing Values

Score = proportion of missing values removed.

#### Task 2 — Fix Missing + Outliers

Score = average of missing + outlier cleaning.

#### Task 3 — Full Cleaning with Efficiency

Score = quality × efficiency bonus.

---

### 🔹 Continuous Grading

Agents receive a score between **0 and 1** instead of binary success.

---

### 🔥 Corruption Events (Key Differentiator)

Every 5 steps:

* New missing values appear
* New outliers appear

This simulates real-world evolving datasets.

---

## 🔌 API Endpoints

* `POST /reset` — Initialize environment
* `POST /step` — Execute action
* `GET /tasks` — List available tasks
* `POST /grader` — Evaluate performance
* `GET /state` — Get current state
* `GET /docs` — Swagger UI

---

## 🧪 Example Usage

### Reset

```bash
POST /reset
```

---

### Step

```json
POST /step
{
  "action": {
    "action_type": "fill_missing",
    "column": "age"
  }
}
```

---

### Grader

```json
POST /grader
{
  "task_id": "task1",
  "data": {...},
  "initial": {...},
  "steps": 5
}
```

---

## ⚙️ Running Locally

```bash
uv run server
```

Then open:

```
http://127.0.0.1:8000/docs
```

---

## 🐳 Building Docker Image

```bash
docker build -t data-clean-rl -f server/Dockerfile .
```

---

## ☁️ Deploying to Hugging Face Spaces

```bash
openenv push --repo-id your-username/data-clean-rl
```

After deployment, your environment will be available at:

```
https://huggingface.co/spaces/<your-username/data-clean-rl>
```

---

## 🔗 Client Usage Example

```python
from my_env import MyEnv, MyAction

with MyEnv(base_url="http://localhost:8000") as env:
    result = env.reset()

    result = env.step(MyAction(action_type="fill_missing", column="age"))
    print(result.observation, result.reward)
```

---

## 🧠 Why This Project Stands Out

* Randomized datasets (no hardcoding)
* Dynamic corruption events
* Continuous scoring system
* Multi-step decision making
* Real-world relevance (data cleaning pipelines)

---

## 📂 Project Structure

```
my_env/
├── models.py
├── server/
│   ├── my_env_environment.py
│   ├── tasks.py
│   ├── app.py
├── README.md
├── Dockerfile
└── openenv.yaml
```

---

## 👨‍💻 Author

Jaya Sandeep Narasimha Chowdhary Nadipalli
M.Tech Data Science & AI
IIT Tirupati

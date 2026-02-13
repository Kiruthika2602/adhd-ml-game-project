import pandas as pd

def preprocess_dataset(path):
    df = pd.read_csv(path)

    # 1️⃣ STANDARDIZE COLUMN NAMES (strip spaces)
    df.columns = df.columns.str.strip()

    # 2️⃣ RENAME COLUMNS SAFELY
    column_mapping = {
        "Daydreaming": "Daydream",
        "ScreenTimeHours": "ScreenTime",
        "FamilyHistoryADHD": "FamilyHistory",
        "Education": "EducationStage"
    }

    for old_col, new_col in column_mapping.items():
        if old_col in df.columns:
            df.rename(columns={old_col: new_col}, inplace=True)

    # 3️⃣ ENSURE REQUIRED COLUMNS EXIST
    required_cols = [
        "InattentionScore", "HyperactivityScore", "ImpulsivityScore",
        "Age", "Gender", "EducationStage",
        "SleepHours", "ScreenTime", "Daydream", "FamilyHistory", "ADHD"
    ]

    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column in dataset: {col}")

    # 4️⃣ ENCODE GENDER (ROBUST)
    df["Gender"] = (
        df["Gender"]
        .astype(str)
        .str.strip()
        .str.lower()
        .map({"male": 1, "female": 0})
    )

    # 5️⃣ ENCODE EDUCATION STAGE (ROBUST)
    edu_map = {
        "child": 0,
        "teen": 1,
        "undergrad": 2,
        "adult": 3
    }

    df["EducationStage"] = (
        df["EducationStage"]
        .astype(str)
        .str.strip()
        .str.lower()
        .map(edu_map)
    )

    # 6️⃣ ENCODE BINARY COLUMNS (ROBUST)
    binary_map = {
        "yes": 1, "no": 0,
        "1": 1, "0": 0,
        1: 1, 0: 0
    }

    for col in ["Daydream", "FamilyHistory"]:
        df[col] = (
            df[col]
            .astype(str)
            .str.strip()
            .str.lower()
            .map(binary_map)
        )

    # 7️⃣ RECOMPUTE SYMPTOM SUM (AUTHORITATIVE)
    df["SymptomSum"] = (
        df["InattentionScore"] +
        df["HyperactivityScore"] +
        df["ImpulsivityScore"]
    )

    # 8️⃣ FINAL CLEANUP
    df = df.fillna(0)

    return df

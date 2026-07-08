import pandas as pd
from groq import Groq

# ==========================================
# Configure Groq API
# ==========================================

API_KEY = "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"

client = Groq(api_key=API_KEY)

# ==========================================
# Read Excel File
# ==========================================

FILE_NAME = "manufacturing_defects_root_causes.xlsx"

df = pd.read_excel(FILE_NAME)

# Last column is Summary
SUMMARY_COLUMN = df.columns[-1]

# Five columns before Summary are Root Causes
ROOT_CAUSE_COLUMNS = df.columns[-6:-1]

print("Root Cause Columns:")
print(ROOT_CAUSE_COLUMNS.tolist())

print("Summary Column:")
print(SUMMARY_COLUMN)


# ==========================================
# Function to Generate Summary
# ==========================================

def generate_summary(root_causes):

    root_causes = [
        str(cause).strip()
        for cause in root_causes
        if pd.notna(cause) and str(cause).strip() != ""
    ]

    if len(root_causes) == 0:
        return ""

    combined_text = "\n".join(root_causes)

    prompt = f"""
You are an experienced manufacturing quality engineer.

Below are multiple root causes describing the same manufacturing issue.

Create ONE concise professional summary.

Rules:
- Combine all points.
- Remove repetition.
- Preserve all important technical details.
- Write only ONE sentence.
- Return ONLY the summary.

Root Causes:

{combined_text}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("API Error:", str(e))
        return "Summary could not be generated."

# ==========================================
# Generate Summaries
# ==========================================

print("Generating summaries...")

for index in df.index:

    print(f"Processing Row {index + 1}")

    causes = df.loc[index, ROOT_CAUSE_COLUMNS].tolist()

    summary = generate_summary(causes)

    df.at[index, SUMMARY_COLUMN] = summary

    print("Completed")

df.to_excel(FILE_NAME, index=False)

print("Completed Successfully!")
print("Summary column has been updated in the same Excel file.")

# Data Cleaning Requirements

## Required Columns
- A0 → student_level
- AX → student_type
- AJ → program
- AW → cumulative_gpa
- BA → credits_earned
- T → gender
- AC → ftic_cohort

## Steps
1. Remove first ~18 metadata rows.
2. Set row 19 as header row.
3. Standardize column names.
4. Normalize categorical values:
   - First Time in College → FTIC
   - Transfer → TR
   - Male / Female → M / F
5. Convert GPA and credits to numeric.
6. Drop rows missing required fields.

## Extracted Filters
Excel filters are preserved using openpyxl and stored as JSON.

import sqlite3

# Connect to DB
conn = sqlite3.connect("candidates.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS candidates (
    StudentName TEXT,
    CollegeName TEXT,
    Round1Marks FLOAT,
    Round2Marks FLOAT,
    Round3Marks FLOAT,
    TechnicalRoundMarks FLOAT,
    TotalMarks FLOAT,
    Result TEXT
)
""")

# Helper functions
def get_float_input(prompt, min_val, max_val):
    while True:
        try:
            val = float(input(prompt))
            if min_val <= val <= max_val:
                return val
            else:
                print(f"Enter value between {min_val} and {max_val}")
        except ValueError:
            print("Enter numeric value.")

def get_text_input(prompt, max_length):
    while True:
        val = input(prompt).strip()
        if len(val) <= max_length:
            return val
        else:
            print(f"Max {max_length} characters allowed.")

# Add multiple students
while True:
    print("\n--- Enter Candidate Details ---")
    student_name = get_text_input("Enter the student's name: ", 30)
    college_name = get_text_input("Enter the college name: ", 50)
    round1_marks = get_float_input("Enter Round 1 marks (0-10): ", 0, 10)
    round2_marks = get_float_input("Enter Round 2 marks (0-10): ", 0, 10)
    round3_marks = get_float_input("Enter Round 3 marks (0-10): ", 0, 10)
    technical_round_marks = get_float_input("Enter Technical Round marks (0-20): ", 0, 20)

    total_marks = round1_marks + round2_marks + round3_marks + technical_round_marks
    result = "Selected" if total_marks >= 35 else "Rejected"

    cursor.execute("""
    INSERT INTO candidates (StudentName, CollegeName, Round1Marks, Round2Marks, Round3Marks, TechnicalRoundMarks, TotalMarks, Result)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (student_name, college_name, round1_marks, round2_marks, round3_marks, technical_round_marks, total_marks, result))

    conn.commit()

    more = input("Add another student? (y/n): ").strip().lower()
    if more != 'y':
        break

# Show ranked list
cursor.execute("""
SELECT 
    RANK() OVER (ORDER BY TotalMarks DESC) AS Rank,
    StudentName, CollegeName, TotalMarks, Result
FROM candidates
ORDER BY Rank ASC
""")

print("\n== Candidate List with Rank & Result ==")
print(f"{'Rank':<5} {'Name':<15} {'College':<15} {'Total Marks':<12} {'Result':<10}")
print("-" * 60)
for row in cursor.fetchall():
    print(f"{row[0]:<5} {row[1]:<15} {row[2]:<15} {row[3]:<12} {row[4]:<10}")

conn.close()

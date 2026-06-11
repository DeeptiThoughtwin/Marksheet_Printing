from datetime import datetime
import psycopg2

class Marksheet:
    def __init__(self):
        while True:
            self.registrtion_no = self.numeric_input("Enter Registration no.: ")
            if len(self.registrtion_no) == 10:
                break  
            print("Error: Please Enter Exact 10 digits please Try Again.")

        self.serial_no = self.numeric_input("Enter Serial no.: ")

        while True:
            self.roll_no = self.numeric_input("Enter Roll No.: ")
            if len(self.roll_no) == 10:
                break  
            print("Error: Roll No. Should be 10 digits please Try Again.")

        while True:
            self.name = self.alpha_input("Enter Your Name: ")
            if len(self.name) <= 25:
                break  
            print("Error: Incorrect Name Try Again.")

        while True:
            self.father_name = self.alpha_input("Enter Father's Name: ")
            if len(self.father_name) <= 25:
                break  
            print("Error: Incorrect Name Try Again.")

        while True:
            self.mother_name = self.alpha_input("Enter Your Mother's Name: ")
            if len(self.mother_name) <= 25:
                break  
            print("Error: Incorrect Name Try Again.")

        while True:
            dob = input("Enter Your Date of Birth (DD/MM/YYYY): ")
            try:
                self.dob_object = datetime.strptime(dob, "%d/%m/%Y").date()
                # FIX 1: Keep it as a Python date object (psycopg2 sends this perfectly to PostgreSQL)
                self.date_of_birth = self.dob_object 
                break  
            except ValueError:
                print("Invalid DOB. Enter using DD/MM/YYYY.")

        self.school_name = self.alpha_input("Enter Your School Name: ")
        self.subjects = []
        self.grand_total = 0
        self.percentage = 0.0
        self.result = "FAIL"

    def numeric_input(self, data):
        while True:
            value = input(data).strip()
            if value.isdigit():
                return value
            print("Invalid input enter digits only.")         

    def alpha_input(self, data):
        while True:
            value = input(data).strip()
            if value.replace(" ", "").isalpha():
                return value
            print("Invalid input enter letters only.")

    def get_subject_details(self):
        while True:
            num = input("Enter Number of Subjects (Max 6): ")
            if num.isdigit() and 0 < int(num) <= 6:
                num_subjects = int(num)
                break
            print("Please enter a valid number of subjects (1 to 6).")

        inserted_subjects = [] 

        for i in range(num_subjects):
            print(f"\nSubject {i+1}")
            
            while True:
                subject = self.alpha_input("Subject Name: ").strip()
                if not subject:
                    print("Error: Name cannot be blank.")
                elif subject.lower() in [s.lower() for s in inserted_subjects]:
                    print("Error: You already added this subject.")
                else:
                    inserted_subjects.append(subject)
                    break

            while True:
                t = input("Theory Marks (Max 80): ").strip()
                p = input("Practical Marks (Max 20): ").strip()
                
                if t.isdigit() and p.isdigit():
                    theory = int(t)
                    practical = int(p)
                    if theory <= 80 and practical <= 20:
                        break
                    print("Please Enter Theory Marks <= 80 and practical <= 20")
                else:
                    print("Marks must be numeric numbers. Try again.")

            total = theory + practical
            self.grand_total += total

            if total >= 90: grade = "A+"
            elif total >= 75: grade = "A"
            elif total >= 60: grade = "B"
            elif total >= 40: grade = "C"
            else: grade = "F"

            self.subjects.append({
                "subject": subject, "theory": theory, 
                "practical": practical, "total": total, "grade": grade
            })

    def calculate_result(self):
        self.percentage = self.grand_total / len(self.subjects) if self.subjects else 0
        self.result = "PASS"
        for sub in self.subjects:
            if sub["total"] < 33:
                self.result = "FAIL"
                break

    def save_to_database(self):
        connection = None
        cursor = None
        try:
            connection = psycopg2.connect(
                dbname="postgres",
                user="postgres",
                password="Root@123",
                host="localhost",
                port="5432"
            )
            cursor = connection.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS marksheets (
                    roll_no VARCHAR(10) PRIMARY KEY,
                    registration_no VARCHAR(10) NOT NULL,
                    serial_no VARCHAR(50),
                    name VARCHAR(25) NOT NULL,
                    father_name VARCHAR(25) NOT NULL,
                    mother_name VARCHAR(25) NOT NULL,
                    date_of_birth DATE NOT NULL,
                    school_name VARCHAR(100) NOT NULL,
                    grand_total INTEGER NOT NULL,
                    percentage NUMERIC(5, 2) NOT NULL,
                    result VARCHAR(4) NOT NULL CHECK (result IN ('PASS', 'FAIL'))
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS student_subjects (
                    id SERIAL PRIMARY KEY,
                    roll_no VARCHAR(10) NOT NULL REFERENCES marksheets(roll_no) ON DELETE CASCADE,
                    subject_name VARCHAR(50) NOT NULL,
                    theory_marks INTEGER NOT NULL CHECK (theory_marks BETWEEN 0 AND 80),
                    practical_marks INTEGER NOT NULL CHECK (practical_marks BETWEEN 0 AND 20),
                    total_marks INTEGER NOT NULL CHECK (total_marks BETWEEN 0 AND 100),
                    grade VARCHAR(2) NOT NULL,
                    CONSTRAINT unique_roll_subject UNIQUE (roll_no, subject_name)
                );
            """)

            student_query = """
            INSERT INTO marksheets (roll_no, registration_no, serial_no, name, father_name, mother_name, date_of_birth, school_name, grand_total, percentage, result)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (roll_no) DO UPDATE SET
                registration_no = EXCLUDED.registration_no,
                serial_no = EXCLUDED.serial_no,
                name = EXCLUDED.name,
                father_name = EXCLUDED.father_name,
                mother_name = EXCLUDED.mother_name,
                date_of_birth = EXCLUDED.date_of_birth,
                school_name = EXCLUDED.school_name,
                grand_total = EXCLUDED.grand_total,
                percentage = EXCLUDED.percentage,
                result = EXCLUDED.result;
            """
            
            student_data = (
                self.roll_no, self.registrtion_no, self.serial_no, self.name,
                self.father_name, self.mother_name, self.date_of_birth, self.school_name,
                self.grand_total, self.percentage, self.result
            )
            cursor.execute(student_query, student_data)

            cursor.execute("DELETE FROM student_subjects WHERE roll_no = %s;", (self.roll_no,))

            subject_query = """
            INSERT INTO student_subjects (roll_no, subject_name, theory_marks, practical_marks, total_marks, grade)
            VALUES (%s, %s, %s, %s, %s, %s);
            """
            for sub in self.subjects:
                
                subject_data = (
                    self.roll_no, 
                    sub["subject"], 
                    sub["theory"], 
                    sub["practical"], 
                    sub["total"], 
                    sub["grade"]
                )
                cursor.execute(subject_query, subject_data)

            connection.commit()
            print("\n[Database Success] Marksheet record saved successfully to PostgreSQL database!")

        
        except Exception as error:
            print(f"\n[Database Error] Failed to save data: {error}")
            if connection:
                connection.rollback()
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()


if __name__ == "__main__":
    m = Marksheet()
    m.get_subject_details()
    m.calculate_result()
    m.save_to_database()

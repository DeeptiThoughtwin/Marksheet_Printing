class Marksheet:
    def __init__(self):
      
      
        # self.marksheet_no = int(input("Enter Marksheet_no: ")).isdigit()
        self.registrtion_no = self.numeric_input("Enter Registration no.: ")
        self.roll_no = self.numeric_input("Enter Your Roll Number: ")
        self.name = self.alpha_input("Enter Your Name: ")
        self.father_name = self.alpha_input("Enter Your Father's Name: ")
        self.mother_name = self.alpha_input("Enter Your Mother's Name: ")
        self.date_of_birth = self.numeric_input("Enter Your Date of Birth (DD/MM/YYYY): ")
        self.school_name = self.alpha_input("Enter Your School Name: ")

        self.subjects = []
        self.grand_total = 0


    def numeric_input(self, data):
        while True:
            value = input(data)
            if value.isdigit():
                return value
            else:
                print("Invalid input! Please enter digits only.")
                break

    def alpha_input(self, data):
        while True:
            value = input(data)
            if value.replace(" ", "").isalpha():
                return value
            else:
                print("Invalid input! Please enter letters only.")
                break


    def get_subject_details(self):
        num_subjects = int(input("Enter Number of Subjects: "))

        for i in range(num_subjects):
            print(f"\nSubject {i+1}")

            subject = input("Subject Name: ")
            theory = int(input("Theory Marks: "))
            practical = int(input("Practical Marks: "))

            total = theory + practical
            self.grand_total += total

            if total >= 90:
                grade = "A+"
            elif total >= 75:
                grade = "A"
            elif total >= 60:
                grade = "B"
            elif total >= 40:
                grade = "C"
            else:
                grade = "F"

            self.subjects.append({
                "subject": subject,
                "theory": theory,
                "practical": practical,
                "total": total,
                "grade": grade
            })

    def calculate_result(self):
        self.percentage = self.grand_total / len(self.subjects)

        self.result = "PASS"

        for sub in self.subjects:
            if sub["total"] < 33:
                self.result = "FAIL"
                break

    def display_marksheet(self):
        print("\n")

        print("="*85)
        print(f"{'registrtion_no':>70} : {self.registrtion_no}")

        print(f"|  {'MARKSHEET':^95} | ")
        print(f"|  {'':^95} | ")
        print(f"|  {'':^95} | ")
        print(f"|  {'':^95} | ")

        print("=" * 85)
        
        
        print(f"| {'Central Board of Secondary Education':^75} | ")
        print(f"| {'CERTIFICATE CUM MARKSHEET':^75} | ")
        print("=" * 85)

        
        print(f"| Roll Number : {self.roll_no} | ")
        print(f"| Student Name : {self.name} | ")
        print(f"| Father's Name : {self.father_name} | ")
        print(f"| Mother's Name : {self.mother_name} | ")
        print(f"| Date of Birth : {self.date_of_birth} | ")
        print(f"| School Name : {self.school_name} | ")


        print("-" * 85)
        print(f"| {'S.No':<4} | {'Subject':<20} | {'Obtained Marks':^30} | {'Grade':<5} |")
        print(f"| {'':<4} | {'':<20} | {'Theory':<8} | {'Practical':<10} | {'Total':<6} | {'':<5} |")
        print("-" * 85)

        for i, sub in enumerate(self.subjects, start=1):
            print(
                f"| {i:<4} | "
                f"{sub['subject']:<20} | "
                f"{sub['theory']:<8} | "
                f"{sub['practical']:<10} | "
                f"{sub['total']:<6} | "
                f"{sub['grade']:<5} |"
            )

        print("=" * 85)

        print(f"| Grand Total : {self.grand_total} | ")
        print(f"| Percentage : {self.percentage:.2f}% | ")
        print(f"| Result : {self.result} | ")

        print("=" * 85)



student = Marksheet()
student.get_subject_details()
student.calculate_result()
student.display_marksheet()




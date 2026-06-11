
from datetime import datetime

class Marksheet:
    def __init__(self):


        while True:
            self.registrtion_no = self.numeric_input("Enter Registration no.:")
            
            if len(self.registrtion_no) == 10:
                
                break  
                
            print("Error: Input is Not valid please Try Again.")



        while True:
            self.serial_no = self.numeric_input("Enter Serial no.:")
            
            if len(self.serial_no) == 10:
                break  
                
            print("Error: Input is Not valid please Try Again.")


        while True:
            self.roll_no = self.numeric_input("Enter Roll No.:")
            
            if len(self.roll_no) == 10:
                break  
                
            print("Error: Input is Not valid please Try Again.")



        while True:
            self.name = self.alpha_input("Enter Your Name: ")
            
            if len(self.name) <= 20:
                break  
                
            print("Error: Incorrect Name Try Again.")



        while True:
            self.father_name = self.alpha_input("Enter Father's Name.:")
            
            if len(self.father_name) <= 25:
                break  
                
            print("Error: Incorrect Name Try Again.")


        while True:
            self.mother_name = self.alpha_input("Enter Your Mother's Name:")
            
            if len(self.mother_name) <= 20:
                break  
                
            print("Error: Incorrect Name Try Again.")


        while True:
            dob = input("Enter Your Date of Birth (DD/MM/YYYY): ")
            try:
                dob_object = datetime.strptime(dob, "%d/%m/%Y").date()
                self.date_of_birth = dob_object.strftime("%d/%m/%Y")
                break  
            except ValueError:
                print("Invalid DOB.Enter using DD/MM/YYYY.")

        self.school_name = self.alpha_input("Enter Your School Name: ")
        self.subjects = []
        self.grand_total = 0

    

    def numeric_input(self, data):
        while True:
            value = input(data)
            if value.isdigit():
                return value
            print("Invalid input enter digits only.")         



    def alpha_input(self, data):
        while True:
            value = input(data)
            if value.replace(" ", "").isalpha():
                return value
            print("Invalid input enter letters only.")
   

     
        

    def get_subject_details(self):
        while True:
            num = input("Enter Number of Subjects: ")
            if num.isdigit() and int(num) > 0:
                num_subjects = int(num)
                break
            print("Please enter a valid number of subjects.")

        for i in range(num_subjects):
            print(f"\nSubject {i+1}")
            subject = self.alpha_input("Subject Name: ")
            
            while True:
                t = input("Theory Marks: ")
                p = input("Practical Marks: ")
                if t.isdigit() and p.isdigit():
                    theory = int(t)
                    practical = int(p)
                    break
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

    def display_marksheet(self):
        col_widths = [6, 22, 11, 13, 11, 12]
        
        
        lines = []
        lines.append(f"Registration No : {self.registrtion_no}")
        lines.append("")
        lines.append(f"{'MARKSHEET':^100}")
        lines.append("=" * 100)
        lines.append(f"{'Central Board of Secondary Education':^100}")
        lines.append(f"{'CERTIFICATE CUM MARKSHEET':^100}")
        lines.append("=" * 100)

        line = f"Student Name  : {self.name}".ljust(80 - len(f"Serial Number   : {self.serial_no}")) + f"Serial Number   : {self.serial_no}"
        lines.append(line)

        line = f"Father's Name : {self.father_name}".ljust(80 - len(f"Roll Number   : {self.roll_no}")) + f"Roll Number   : {self.roll_no}"
        lines.append(line)
        
        lines.append(f"Mother's Name : {self.mother_name}")
        lines.append(f"Date of Birth : {self.date_of_birth}")
        lines.append(f"School Name   : {self.school_name}")
        lines.append("-" * 100)




        
        col_widths = [6, 25, 10, 12, 10, 10]

        
        lines.append(
            f"| {'S.No':^{col_widths[0]}} "
            f"| {'Subject':^{col_widths[1]}} "
            f"| {'Theory':^{col_widths[2]}} "
            f"| {'Practical':^{col_widths[3]}} "
            f"| {'Total':^{col_widths[4]}} "
            f"| {'Grade':^{col_widths[5]}} |"
        )

        
        total_width = sum(col_widths) + (len(col_widths) * 3) + 1
        lines.append("-" * total_width)

       
        for i, sub in enumerate(self.subjects, start=1):
            lines.append(
                f"| {i:<{col_widths[0]}} "
                f"| {sub['subject']:^{col_widths[1]}} "
                f"| {sub['theory']:^{col_widths[2]}} "
                f"| {sub['practical']:^{col_widths[3]}} "
                f"| {sub['total']:^{col_widths[4]}} "
                f"| {sub['grade']:^{col_widths[5]}} |"
            )


        lines.append("=" * 100)

        line = f"Grand Total : {self.grand_total}".ljust(80 - len(f"Result : {self.result}")) + f"Result : {self.result}"
        lines.append(line)

      
        lines.append(f"Percentage  : {self.percentage:.2f}%")
        
        lines.append("=" * 100)

        max_len = max(len(line) for line in lines)
        box_width = max_len + 4 

        print("\n" + "-" * box_width)
        for line in lines:
            print(f"| {line:<{max_len}} |")
        print("-" * box_width + "\n")


student = Marksheet()
student.get_subject_details()
student.calculate_result()
student.display_marksheet()






   
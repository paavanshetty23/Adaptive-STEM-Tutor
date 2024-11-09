import fpdf
import os

class PDF(fpdf.FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'STEM Practice Problems Collection', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_stem_pdf():
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Mathematics Section
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Mathematics', 0, 1, 'L')
    pdf.ln(5)

    pdf.set_font('Arial', '', 12)
    math_problems = [
        {
            "title": "Beginner: Basic Algebra",
            "problem": "Solve for x: 3x + 7 = 22",
            "solution": "Step 1: Subtract 7 from both sides: 3x = 15\nStep 2: Divide both sides by 3: x = 5"
        },
        {
            "title": "Intermediate: Quadratic Equations",
            "problem": "Solve the quadratic equation: x² - 5x + 6 = 0",
            "solution": "Using factoring: (x - 2)(x - 3) = 0\nTherefore, x = 2 or x = 3"
        },
        {
            "title": "Advanced: Calculus",
            "problem": "Find the derivative of f(x) = 3x⁴ - 2x³ + 5x - 1",
            "solution": "f'(x) = 12x³ - 6x² + 5"
        }
    ]

    for problem in math_problems:
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, problem["title"], 0, 1, 'L')
        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 10, f"Problem:\n{problem['problem']}\n\nSolution:\n{problem['solution']}\n")
        pdf.ln(5)

    # Physics Section
    pdf.add_page()
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Physics', 0, 1, 'L')
    pdf.ln(5)

    physics_problems = [
        {
            "title": "Beginner: Kinematics",
            "problem": "A car travels at a constant speed of 60 km/h. How far will it travel in 2.5 hours?",
            "solution": "Using d = vt\nDistance = 60 km/h × 2.5 h = 150 km"
        },
        {
            "title": "Intermediate: Forces",
            "problem": "A 5 kg mass is suspended by two ropes at angles of 30° and 45° to the horizontal. Find the tension in each rope.",
            "solution": "Using force balance equations:\nT1 cos(30°) = T2 cos(45°)\nT1 sin(30°) + T2 sin(45°) = 49 N\nSolving: T1 = 35.7 N, T2 = 30.9 N"
        },
        {
            "title": "Advanced: Electromagnetics",
            "problem": "A straight wire of length 2m carries a current of 5A in a magnetic field of 0.5T perpendicular to the wire. Calculate the force on the wire.",
            "solution": "Using F = BIL\nF = 0.5T × 5A × 2m = 5N"
        }
    ]

    for problem in physics_problems:
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, problem["title"], 0, 1, 'L')
        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 10, f"Problem:\n{problem['problem']}\n\nSolution:\n{problem['solution']}\n")
        pdf.ln(5)

    # Chemistry Section
    pdf.add_page()
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Chemistry', 0, 1, 'L')
    pdf.ln(5)

    chemistry_problems = [
        {
            "title": "Beginner: Balancing Equations",
            "problem": "Balance the following chemical equation: H2 + O2 → H2O",
            "solution": "Balanced equation: 2H2 + O2 → 2H2O"
        },
        {
            "title": "Intermediate: Stoichiometry",
            "problem": "How many grams of oxygen (O2) are needed to completely react with 10 grams of hydrogen (H2) to form water?",
            "solution": "Using balanced equation: 2H2 + O2 → 2H2O\nMolar mass H2 = 2g/mol, O2 = 32g/mol\n10g H2 × (1 mol H2/2g H2) × (1 mol O2/2 mol H2) × (32g O2/1 mol O2) = 80g O2"
        },
        {
            "title": "Advanced: Equilibrium",
            "problem": "For the reaction N2 + 3H2 ⇌ 2NH3, the equilibrium constant Kc = 0.5 at 400°C. Calculate the equilibrium concentrations if initial concentrations are [N2]0 = 0.8M, [H2]0 = 0.6M, and [NH3]0 = 0.",
            "solution": "Using ICE table and equilibrium equations:\nAt equilibrium: [N2] = 0.65M, [H2] = 0.35M, [NH3] = 0.3M"
        }
    ]

    for problem in chemistry_problems:
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, problem["title"], 0, 1, 'L')
        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 10, f"Problem:\n{problem['problem']}\n\nSolution:\n{problem['solution']}\n")
        pdf.ln(5)

    # Save the PDF
    pdf.output('stem_problems.pdf')

if __name__ == "__main__":
    generate_stem_pdf()
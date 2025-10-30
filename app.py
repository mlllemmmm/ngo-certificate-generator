import streamlit as st
from fpdf import FPDF
from datetime import datetime

# Certificate Generator Function
def generate_certificate(name, gender, duration, task, email, issue_date):
    # Set pronouns based on gender
    pronoun_he_she = "he" if gender == "Male" else "she"
    pronoun_his_her = "his" if gender == "Male" else "her"

    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()

    # Add certificate background image
    try:
        pdf.image("certificate_template.png", x=0, y=0, w=210, h=297)
    except:
        pdf.set_font("Arial", "B", 20)
        pdf.cell(0, 10, "Certificate Template Missing", ln=True, align="C")

    # Recipient Name (less bold + small gap before line)
    pdf.set_xy(0, 115)
    pdf.set_font("Arial", "B", 24)  # reduced font weight slightly
    pdf.cell(210, 10, name, align="C")

    # Add a subtle gap (the underline will now have a bit of breathing space)
    pdf.set_xy(25, 135)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 8, f"Work Duration: {duration}\nTask Performed: {task.upper()}")

    # Certificate Body Text
    text = (
        f"This letter certifies that {name} is a volunteer and has contributed {pronoun_his_her} time "
        f"and effort to Akshar Paaul. During {pronoun_his_her} time with us, {pronoun_he_she} remained "
        f"dedicated and loyal to {pronoun_his_her} work and responsibilities. "
        f"{pronoun_he_she.capitalize()} performed {pronoun_his_her} duties with excellence and always "
        f"maintained a professional and courteous attitude and appearance. "
        f"We wish {pronoun_his_her} the best of luck in {pronoun_his_her} future endeavors."
    )

    pdf.set_xy(25, 155)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(160, 8, text)

    # Issue Date (moved upward slightly)
    formatted_date = issue_date.strftime('%d-%m-%Y')
    pdf.set_xy(25, 232)  # previously 240, now raised a bit higher
    pdf.set_font("Arial", "I", 11)
    pdf.cell(0, 10, f"Issue Date: {formatted_date}", align="L")

    # Save the PDF
    file_name = f"Volunteer_Certificate_{name.replace(' ', '_')}.pdf"
    pdf.output(file_name)
    return file_name


# Streamlit App
def main():
    st.title("🎓 Akshar Paaul Volunteer Certificate Generator")

    st.subheader("Enter Volunteer Details Below")

    # Input Fields
    name = st.text_input("Recipient Name")
    gender = st.selectbox("Gender", ["Male", "Female"])
    duration = st.number_input("Work Duration (hours)", min_value=1, step=1)
    task = st.text_input("Task Performed")
    email = st.text_input("Recipient Email")
    issue_date = st.date_input("Issue Date", value=datetime.today())

    # Generate Button
    if st.button("Generate Certificate"):
        if name.strip() and task.strip() and email.strip():
            cert_file = generate_certificate(name, gender, duration, task, email, issue_date)
            with open(cert_file, "rb") as f:
                st.download_button("⬇️ Download Certificate", f, file_name=cert_file)
        else:
            st.warning("⚠️ Please fill all fields before generating the certificate.")


if __name__ == "__main__":
    main()

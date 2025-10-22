import streamlit as st
from fpdf import FPDF
from datetime import datetime

# Certificate Generator Function
def generate_certificate(name, role, hours=None, cert_type="Volunteer"):
    # Use portrait mode (since your template is vertical)
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()

    # Add the certificate template image
    try:
        pdf.image("certificate_template.png", x=0, y=0, w=210, h=297)
    except:
        pdf.set_font("Arial", "B", 20)
        pdf.cell(0, 10, f"{cert_type} Certificate (Template Missing)", ln=True, align="C")

    # Recipient Name (centered in the middle of the page)
    pdf.set_xy(0, 120)
    pdf.set_font("Arial", "B", 28)
    pdf.cell(210, 10, name, align="C")

    # Role and Hours (depending on type)
    pdf.set_xy(0, 140)
    pdf.set_font("Arial", "", 16)
    if cert_type == "Volunteer":
        pdf.cell(210, 10, f"For {hours} hours of service as {role}", align="C")
    else:
        pdf.cell(210, 10, f"For successfully completing Internship as {role}", align="C")

    # Date (lower section)
    pdf.set_xy(0, 160)
    pdf.set_font("Arial", "I", 12)
    pdf.cell(210, 10, f"Issued on {datetime.today().strftime('%d-%m-%Y')}", align="C")

    # Save the PDF
    file_name = f"{cert_type}_certificate_{name.replace(' ', '_')}.pdf"
    pdf.output(file_name)
    return file_name

# Streamlit App
def main():
    st.title("🎓 NGO Certificate Generator")

    tab1, tab2 = st.tabs(["Volunteer Certificate", "Internship Certificate"])

    # --- Volunteer Certificate Tab ---
    with tab1:
        st.subheader("Volunteer Certificate Details")
        name = st.text_input("Enter Volunteer Name")
        role = st.text_input("Enter Volunteer Role")
        hours = st.number_input("Enter Hours of Service", min_value=1, step=1)

        if st.button("Generate Volunteer Certificate"):
            if name.strip() and role.strip():
                cert_file = generate_certificate(name, role, hours, cert_type="Volunteer")
                with open(cert_file, "rb") as f:
                    st.download_button("⬇️ Download Volunteer Certificate", f, file_name=cert_file)
            else:
                st.warning("⚠️ Please enter both Name and Role before generating the certificate.")

    # --- Internship Certificate Tab ---
    with tab2:
        st.subheader("Internship Certificate Details")
        name = st.text_input("Enter Intern Name", key="intern_name")
        role = st.text_input("Enter Intern Role", key="intern_role")

        if st.button("Generate Internship Certificate"):
            if name.strip() and role.strip():
                cert_file = generate_certificate(name, role, cert_type="Internship")
                with open(cert_file, "rb") as f:
                    st.download_button("⬇️ Download Internship Certificate", f, file_name=cert_file)
            else:
                st.warning("⚠️ Please enter both Name and Role before generating the certificate.")

if __name__ == "__main__":
    main()

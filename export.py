import mysql.connector
from lxml import etree


def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="globaltech"
    )


def export_to_xml():
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    root = etree.Element("GlobalTechData")

    # Export Projects
    projects_element = etree.SubElement(root, "Projects")

    cursor.execute("SELECT * FROM projects")
    projects = cursor.fetchall()

    for row in projects:
        project = etree.SubElement(projects_element, "Project")

        etree.SubElement(project, "ProjectID").text = str(row["ProjectID"])
        etree.SubElement(project, "ProjectName").text = row["ProjectName"]
        etree.SubElement(project, "Department").text = row["Department"]
        etree.SubElement(project, "StartDate").text = str(row["StartDate"])
        etree.SubElement(project, "Status").text = row["Status"]

    # Export Employees
    employees_element = etree.SubElement(root, "Employees")

    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()

    for row in employees:
        employee = etree.SubElement(employees_element, "Employee")

        etree.SubElement(employee, "EmployeeID").text = str(row["EmployeeID"])
        etree.SubElement(employee, "Name").text = row["Name"]
        etree.SubElement(employee, "Department").text = row["Department"]
        etree.SubElement(employee, "Email").text = row["Email"]
        etree.SubElement(employee, "HireDate").text = str(row["HireDate"])
        etree.SubElement(employee, "ProjectID").text = str(row["ProjectID"])

    # Export Payroll Records
    payroll_records_element = etree.SubElement(root, "PayrollRecords")

    cursor.execute("SELECT * FROM payroll")
    payroll_records = cursor.fetchall()

    for row in payroll_records:
        payroll = etree.SubElement(payroll_records_element, "Payroll")

        etree.SubElement(payroll, "PayrollID").text = str(row["PayrollID"])
        etree.SubElement(payroll, "EmployeeID").text = str(row["EmployeeID"])
        etree.SubElement(payroll, "Month").text = row["Month"]
        etree.SubElement(payroll, "Year").text = str(row["Year"])
        etree.SubElement(payroll, "BasicSalary").text = str(row["BasicSalary"])
        etree.SubElement(payroll, "Bonus").text = str(row["Bonus"])

    tree = etree.ElementTree(root)
    tree.write(
        "globaltech_data.xml",
        pretty_print=True,
        xml_declaration=True,
        encoding="UTF-8"
    )

    cursor.close()
    conn.close()

    print("Data successfully exported to globaltech_data.xml")


if __name__ == "__main__":
    export_to_xml()
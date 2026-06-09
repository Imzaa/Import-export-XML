import mysql.connector
from lxml import etree


def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="globaltech"
    )                


def validate_xml(xml_file, xsd_file):
    xml_doc = etree.parse(xml_file)
    xsd_doc = etree.parse(xsd_file)

    schema = etree.XMLSchema(xsd_doc)
    schema.assertValid(xml_doc)

    return xml_doc


def import_xml():
    xml_file = "globaltech_data.xml"
    xsd_file = "globaltech_schema.xsd"

    try:
        xml_doc = validate_xml(xml_file, xsd_file)
        root = xml_doc.getroot()

        conn = connect_db()
        cursor = conn.cursor()

        conn.start_transaction()

        # Import Projects first
        for project in root.find("Projects").findall("Project"):
            sql = """
                INSERT INTO projects 
                (ProjectID, ProjectName, Department, StartDate, Status)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    ProjectName = VALUES(ProjectName),
                    Department = VALUES(Department),
                    StartDate = VALUES(StartDate),
                    Status = VALUES(Status)
            """

            values = (
                int(project.findtext("ProjectID")),
                project.findtext("ProjectName"),
                project.findtext("Department"),
                project.findtext("StartDate"),
                project.findtext("Status")
            )

            cursor.execute(sql, values)

        # Import Employees second
        for employee in root.find("Employees").findall("Employee"):
            sql = """
                INSERT INTO employees 
                (EmployeeID, Name, Department, Email, HireDate, ProjectID)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    Name = VALUES(Name),
                    Department = VALUES(Department),
                    Email = VALUES(Email),
                    HireDate = VALUES(HireDate),
                    ProjectID = VALUES(ProjectID)
            """

            values = (
                int(employee.findtext("EmployeeID")),
                employee.findtext("Name"),
                employee.findtext("Department"),
                employee.findtext("Email"),
                employee.findtext("HireDate"),
                int(employee.findtext("ProjectID"))
            )

            cursor.execute(sql, values)

        # Import Payroll last
        for payroll in root.find("PayrollRecords").findall("Payroll"):
            sql = """
                INSERT INTO payroll 
                (PayrollID, EmployeeID, Month, Year, BasicSalary, Bonus)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    EmployeeID = VALUES(EmployeeID),
                    Month = VALUES(Month),
                    Year = VALUES(Year),
                    BasicSalary = VALUES(BasicSalary),
                    Bonus = VALUES(Bonus)
            """

            values = (
                int(payroll.findtext("PayrollID")),
                int(payroll.findtext("EmployeeID")),
                payroll.findtext("Month"),
                int(payroll.findtext("Year")),
                float(payroll.findtext("BasicSalary")),
                float(payroll.findtext("Bonus"))
            )

            cursor.execute(sql, values)

        conn.commit()

        print("XML data successfully imported into the database.")

    except Exception as e:
        if "conn" in locals() and conn.is_connected():
            conn.rollback()

        print("Import failed. Transaction rolled back.")
        print("Error:", e)

    finally:
        if "cursor" in locals():
            cursor.close()

        if "conn" in locals() and conn.is_connected():
            conn.close()


if __name__ == "__main__":
    import_xml()
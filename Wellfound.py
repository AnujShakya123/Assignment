import imaplib
import email
from email.header import decode_header
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Email credentials
email_user = "anujshakya808@gmail.com"
email_password = "ymnt dvse udva cyuv"
imap_server = "imap.gmail.com"

def get_latest_otp_from_email():
    # Set up the IMAP connection
    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(email_user, email_password)
    mail.select("inbox")

    # Search for unread emails
    status, messages = mail.search(None, '(UNSEEN)')
    mail_ids = messages[0].split()

    if not mail_ids:
        print("No unread emails found.")
        return None

    # Fetch the latest unread email
    latest_email_id = mail_ids[-1]
    status, msg_data = mail.fetch(latest_email_id, "(RFC822)")

    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])
            subject = decode_header(msg["Subject"])[0][0]
            if isinstance(subject, bytes):
                subject = subject.decode()

            print(f"Subject: {subject}")
            
            # Assuming OTP is in the email body, we search for it using regex
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if content_type == "text/plain":
                        body = part.get_payload(decode=True).decode()
                        print(f"Body: {body}")
                        otp_match = re.search(r"\b\d{4}\b", body)  # Regex to find a 4-digit OTP
                        if otp_match:
                            return otp_match.group(0)
            else:
                body = msg.get_payload(decode=True).decode()
                otp_match = re.search(r"\b\d{4}\b", body)
                if otp_match:
                    return otp_match.group(0)

    return None


# Path to your ChromeDriver executable
driver_path = r"C:\Users\Anuj\AppData\Local\Programs\Python\chromedriver-win64\chromedriver.exe"

# Create a Service object for ChromeDriver
service = ChromeService(executable_path=driver_path)

# Initialize the WebDriver with the Service object
driver = webdriver.Chrome(service=service)

try:
    driver.get("https://sg-app.abouv.com/welcome")
    
    # Wait for page to load and click on "Get Started" or similar button if needed
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[3]/div/div/a'))).click()

  
    # Handle "Skip and Download" Page
    # Wait for "Skip and Download" button and click it
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[3]/div[2]/button[1]'))).click()


    #  Enter Mobile Number and click "Continue"

    mobile_number_field = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/form/div[3]/div/div/input')))
    print("Entering mobile number...")
    mobile_number_field.send_keys("8171916543")  # Enter your mobile number here

    # Click "Continue"
    continue_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/form/div[5]/div/button')))
    print("Clicking Continue...")
    continue_button.click()

    #Wait for OTP input fields
    print("Waiting for OTP input fields to appear...")
    otp_fields = WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.XPATH, "/html/body/div/div/form/div[2]/div[2]/div/div[1]"))
)

# Submit the OTP
    submit_otp_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/form/div[3]/div/button"))
)
    print("Submitting OTP...")
    submit_otp_button.click()

    # Wait until URL contains 'onboarding' or proceed manually
    WebDriverWait(driver, 10).until(EC.url_contains("onboarding"))


    # Onboarding (hearing category)
    driver.get("https://sg-app.abouv.com/onboarding?category=hear")

    # Wait for the options to be visible (e.g., "Family/Friends")
    print("Waiting for options to appear...")
    option_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div/div[2]/div/div/div[2]'))
    )

    #Select the "Family/Friends" option
    print("Clicking 'Family/Friends' option...")
    option_element.click()

    #Click the "Continue" button
    print("Waiting for 'Continue' button...")
    continue_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div/div[3]/div/div/button'))
    )
    print("Clicking 'Continue' button...")
    continue_button.click()
# Wait until URL contains 'onboarding' or proceed manually
    WebDriverWait(driver, 10).until(EC.url_contains("onboarding"))

#Go to the hearing category page manually if redirection didn't happen
    driver.get("https://sg-app.abouv.com/onboarding?category=hear")

# Wait for the options to be visible (e.g., "Family/Friends")
    print("Waiting for options to appear...")
    option_element = WebDriverWait(driver, 15).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div/div[2]/div/div/div[2]'))
)

# Click the "Family/Friends" option
    print("Clicking 'Family/Friends' option...")
    option_element.click()

# Wait for and click the "Continue" button
    print("Waiting for 'Continue' button...")
    continue_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div/div[3]/div/div/button'))
)
    print("Clicking 'Continue' button...")
    continue_button.click()

    print("Continue button clicked successfully.")
    # Optional: You can wait for the next page to load or handle further steps here
    print("Continue button clicked successfully.")

    # Onboarding (role category)
    driver.get("https://sg-app.abouv.com/onboarding?category=role")
    student_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div/div[2]/div/div/div[2]'))
    )
    
    # Click the "Student" option
    print("Selecting 'Student'...")
    student_option.click()

    # Wait for the "Continue" button to be clickable
    continue_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div/div[3]/div/div/button'))
    )
    
    # Click the "Continue" button
    print("Clicking 'Continue'...")
    continue_button.click()

    print("Successfully selected 'Student' and clicked 'Continue'.")

    # Onboarding (goal category)
    driver.get("https://sg-app.abouv.com/onboarding?category=goal")
        # Wait for the "Job Opportunities" option to be clickable and select it
    job_opportunities_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div/div[2]/div/div/div[2]'))
    )
    print("Selecting 'Job Opportunities'...")
    job_opportunities_option.click()

    # Wait for the "Paid Internships" option to be clickable and select it
    paid_internships_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div/div[2]/div/div/div[3]'))
    )
    print("Selecting 'Paid Internships'...")
    paid_internships_option.click()

    # You can add more options similarly by selecting their corresponding XPaths

    # Wait for the "Continue" button to be clickable
    continue_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div/div[3]/div/div/button'))
    )
    
    # Click the "Continue" button
    print("Clicking 'Continue'...")
    continue_button.click()

    print("Successfully selected goals and clicked 'Continue'.")

    #Profile Setup (choose "Continue with email")
    driver.get("https://sg-app.abouv.com/onboarding?category=profileSetup")
    

    continue_with_email_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div/div[3]/div/div/button[2]'))
    )
    # print("Clicking 'Continue with Email'...")
    # continue_with_email_button.click()
    driver.execute_script("arguments[0].click();", continue_with_email_button)

    #Wait for the next page to load (where the email input is)
    email_input_field = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div/div[2]/div/form/div/div/input'))
    )
    
    # Enter your email address
    email_address = "anujshakya808@gmail.com"  # Replace with your actual email
    print(f"Entering email address: {email_address}")
    email_input_field.send_keys(email_address)

    #Click the "Continue" button on the email input page
    continue_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div/div/div[2]/div/form/button'))
    )
    print("Clicking 'Continue' after entering the email...")
    continue_button.click()

    # Optionally, you can handle the next steps here after submitting the email
    print("Email submitted successfully.")


   # Wait for OTP fields
    print("Waiting for OTP input fields...")
    otp_input_fields = WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.XPATH, '/html/body/div/div/div/div/div[2]/div/div[2]/div[1]'))
    )

   # Print the number of OTP input fields found
    print(f"Number of OTP input fields found: {len(otp_input_fields)}")

# Retrieve the latest OTP from email
    otp_value = get_latest_otp_from_email()

    if otp_value:
     print(f"OTP retrieved: {otp_value}")

    # Check if the length of otp_value matches the number of OTP input fields
    if len(otp_value) == len(otp_input_fields):
        # Input the OTP into the fields
        for i, digit in enumerate(otp_value):
            # Wait for each OTP input field to be clickable
            otp_input_field = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(otp_input_fields[i])
            )

            # Scroll into view
            driver.execute_script("arguments[0].scrollIntoView();", otp_input_field)

            # Send the OTP digit
            otp_input_field.send_keys(digit)

        print("OTP entered successfully.")

    #Click the "Continue" button to submit OTP
    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div/div/div[3]/div/div/button'))
    )
    print("Clicking Continue button...")
    submit_button.click()
    

    # Profile Info (Avoid Add Photo)
    driver.get("https://sg-app.abouv.com/onboarding?category=profileInfo")

    #Fill in "First Name"
    first_name_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/div/form/div[3]/div/div[1]/input'))  # Adjust the XPath based on your page structure
    )
    first_name_field.send_keys("Anuj")

    # Fill in "Last Name"
    last_name_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/div/form/div[3]/div/div[2]/input'))  # Adjust the XPath
    )
    last_name_field.send_keys("Shakya")

    #Fill in "Pin Code"
    pin_code_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/div/form/div[3]/div/div[3]/input'))  # Adjust the XPath
    )
    pin_code_field.send_keys("201016")

 

    # Click the "Continue" button
    continue_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/form/div[4]/div/button'))  # Adjust the XPath
    )
    continue_button.click()
    time.sleep(10)

    print("Profile form successfully automated and submitted!")

    print("Test completed successfully!")

finally:
    # Clean up
    driver.quit()
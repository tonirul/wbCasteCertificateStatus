\# Caste Certificate Status \& Download App

This is a \*\*Flask-based web application\*\* that allows you to:


\- Check the \*\*status\*\* of caste certificate applications (from `https://castcertificatewb.gov.in/application\_search`).

\- Perform \*\*bulk checks\*\* by entering multiple application numbers or uploading a CSV file.

\- Download available \*\*signed certificates (PDF)\*\* directly from the WB Government portal (`https://castcertificatewb.gov.in/downlaod\_signcertificate`).


---



\## 🚀 Features



\- \*\*Single / Bulk Search\*\*

&nbsp; - Enter application numbers manually.

&nbsp; - Upload a `.csv` file with application numbers.

\- \*\*Status Results\*\*

&nbsp; - Displays details like application ID, status description, etc.

\- \*\*Certificate Download\*\*

&nbsp; - If the certificate is ready, download it as a PDF from the portal.



---



\## 📂 Project Structure



project/

│── app.py # Main Flask application

│── templates/

│ └── index.html # Web interface

│── static/ # (Optional) static files (CSS/JS)

│── README.md # Documentation





---



\## 🔧 Requirements



\- Python \*\*3.8+\*\*

\- Flask

\- Requests



---



\## 📦 Installation



1\. Clone this repository or copy the files.



&nbsp;  ```bash

&nbsp;  git clone https://github.com/yourusername/caste-certificate-app.git

&nbsp;  cd caste-certificate-app



(Optional) Create a virtual environment.



python -m venv venv

source venv/bin/activate    # Linux/Mac

venv\\Scripts\\activate       # Windows





Install dependencies.



pip install flask requests



▶️ Running the App



Run the Flask server:



python app.py





By default, it starts at http://127.0.0.1:5000/

.



💻 Usage



Open the app in your browser:

👉 http://127.0.0.1:5000/



Choose one of the following:



Enter application numbers (one per line).



Upload a .csv file with a column ApplicationNumber.



Click Submit.

The app will display application statuses.



If a certificate is ready:



A Download Link will appear.



Clicking it downloads the PDF certificate.



📑 CSV File Format



Your .csv file should look like this:



ApplicationNumber

1234567890

9876543210

1122334455



⚠️ Notes



This project interacts with official WB government servers.



Availability depends on server uptime and response.



Use responsibly for legitimate purposes only.



Debug mode is enabled (debug=True). Disable it in production.



🛠️ Troubleshooting



SSL/TLS errors:

The app uses a custom SSLAdapter to support legacy TLS servers. If you face issues, update requests and urllib3.



Timeouts:

Some requests may take longer if the server is busy. Default timeout is 15 seconds.



📜 License



This project is for educational and personal use only.

Not affiliated with the Government of West Bengal.



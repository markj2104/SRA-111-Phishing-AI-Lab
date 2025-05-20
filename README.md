Full STEP-BY-STEP Project Setup: SRA 111 Phishing & AI Lab

This documentation covers every major step, command, dependency, package, and issue that was resolved during the setup and execution of the SRA 111 Phishing & AI Lab. This is a finalized documentation report that excludes any unnecessary or redundant details. Additionally, specific terminal-based commands will be written in blue text. 

All associated python code can be found in this GitHub repository. 

Initial Project Planning (Context)
To build a phishing detection lab using machine learning on a Jetson Orin Nano with Seeed Studio carrier board, running Ubuntu. The lab uses:
A virtual Python environment
Custom email parsing scripts
Scikit-learn for AI modeling
Datasets: Enron Emails (legitimate) + Honeypot phishing emails
Hardware: 
Device: Jetson Orin Nano by NVIDIA, integrated into a Seeed Studio development board.
OS: Ubuntu 20.04 LTS (arm64 architecture).

Step 1: System Update & Essentials 
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv -y
Additional tools we installed (for development convenience):
sudo apt install git nano wget unzip -y

Step 2: Virtual Environment Setup
cd ~
Start your project from a clean, user-specific location.
python3 -m venv myenv
This command creates a contained Python environment called myenv, where you can install Python packages without affecting system-wide Python. You can pin specific versions of packages that are compatible with your code. This is especially important on Jetson Orin, where system Python is used by the OS and modifying it can break core services. 
source myenv/bin/activate
This command activates the virtual environment. It modifies your terminal session so that Python and pip commands use the virtual environment's versions. Any package installed with pip goes into myenv/lib instead of the global system. You’ll also notice the prompt changes to indicate you're now inside the myenv virtual environment. This ensures you're running your code and installing libraries in the controlled virtual environment — critical for reproducibility and preventing system breakage.

STEP 3: Install Python Dependencies
pip install pandas scikit-learn matplotlib
Pandas is installed for reading, manipulating, and writing CSV files (like emails and labels). Scikit-learn is installed for machine learning: model training (Naive Bayes), testing, and metrics. Matplotlib is installed for visualizing results like accuracy or confusion matrices. These are the core libraries the phishing AI model needs to preprocess data, train the classifier, and evaluate performance.

STEP 4: System Dependencies for lxml and Other C Extensions
While installing the required Python packages (especially lxml and beautifulsoup4), the Jetson Orin threw errors because lxml depends on C-based system libraries which were not installed by default. Without them, pip throws errors like:
fatal error: libxml/parser.h: No such file or directory
xslt-config not found
command 'gcc' failed with exit status 1
sudo apt install libxml2-dev libxslt1-dev python3-dev libffi-dev build-essential -y
Without these, pip install lxml will fail with compiler or missing header errors. The solution is to install required system libraries.
sudo apt install libxml2-dev libxslt1-dev python3-dev libffi-dev build-essential -y
The libxml2-dev command installs core XML parsing headers needed to build lxml. The libxslt1-dev	command is required for XSLT support (used by lxml). The python3-dev command is required for compiling Python C extensions like lxml. The libffi-dev command helps compile Python packages that use foreign function interfaces. Finally, the build-essential	 command installs GCC and core build tools like make, needed to compile packages
Then install Python packages:
pip install --upgrade pip setuptools wheel
pip install pandas scikit-learn beautifulsoup4 lxml

After this, lxml is installed without needing a precompiled wheel (no precompiled wheel available for Jetpack OS versions). You used BeautifulSoup (from beautifulsoup4) for parsing HTML email bodies, to clean, extract, or tokenize text before it is passed to the machine learning model. Beautifulsoup4 uses lxml as a fast and feature-rich parser. Without lxml, it falls back to Python’s built-in HTML parser, which is slower and less robust.


Finally, upgrade the python build tools. This ensures that your build tools can compile the latest Python packages cleanly and prevents common issues like "Could not build wheels for lxml" by ensuring pip uses modern build backends..
pip install --upgrade pip setuptools wheel
Install Python Packages Again (Now with No Errors)
pip install pandas scikit-learn beautifulsoup4 lxml
Now that the system has all required header files and libraries, this command successfully compiles and installs lxml from source.

STEP 5: Project Folder Structure
mkdir phishing_pot
cd phishing_pot
mkdir enron phishing outputs

STEP 6: Get and Prepare Datasets
Enron Email Dataset Source: 
https://www.kaggle.com/datasets/wcukierski/enron-email-dataset 

Phishing Email Dataset Source: 
https://github.com/rf-peixoto/phishing_pot 

Extract emails (we used .txt or .eml files) into:
phishing_pot/enron/

Step 7: Email Parser Script
nano parse_emails.py
python3 parse_emails.py
Wrote Python code using BeautifulSoup and os.walk to:
Read Enron as label=0
Read phishing as label=1
Strip HTML tags
Save a CSV with message, label
Output: outputs/all_emails.csv

STEP 8: Create Balanced Sample for Students
We made a script to pull a small set (e.g., 5 phishing, 5 legit):
nano new_csv.py
python3 new_csv.py


What it does:
From the large dataset, samples a small balanced subset (e.g., 5 phishing, 5 legit)
Saves this subset to outputs/balanced_sampled_emails.csv
Used for student exercises or quick testing

Why this step?
To create a manageable subset of the data for hands-on learning, without overwhelming students with large datasets.

STEP 9: Build & Run Model (test_model.py)
nano test_model.py
python3 test_model.py
Key features: 
Load all_emails.csv
Vectorize using TfidfVectorizer
Train/test split (e.g., 80/20)
Train a MultinomialNB model
Evaluate accuracy
Optionally run predictions on balanced_sampled_emails.csv
Output: Console printout of model accuracy + predictions.

Why this step?
This step trains and evaluates the machine learning model, confirming that the dataset and preprocessing work well and the model performs adequately.

STEP 10: Prepare Enron Dataset
python3 prepare_enron_dataset.py

What it does:
Cleans and processes raw Enron email data
Outputs cleaned CSV (e.g., cleaned_enron_emails.csv)

Why?
Raw Enron emails are messy; this makes the data consistent and ready for merging.

STEP 11: Prepare Phishing Dataset 
python3 prepare_dataset.py

What it does: 
Clean phishing scripts 
STEP 12: Generate Combined Dataset
python3 generate_email_datasets.py

What it does:
Merges cleaned Enron and phishing datasets into one combined file (combined_emails.csv)
Adds proper labels to emails (0 or 1)

Why?
We want a single dataset with both phishing and legitimate emails labeled for training.

STEP 13: Balance the Dataset
python3 balance_classified_emails.py

What it does:
Balances the combined dataset to avoid bias (equal phishing and legit emails)
Saves to balanced_classified_emails.csv

Why?
To prevent the model from being skewed by class imbalance.


STEP 14: Train Classifier
python3 train_classifier.py

What it does:
Vectorizes emails (e.g., TF-IDF)
Trains the model (e.g., MultinomialNB)
Saves the trained model (phishing_model.joblib) and vectorizer (vectorizer.joblib)

Why?
To have a reusable trained model for classification.


STEP 15: Train and Classify
python3 train_and_classify.py

What it does:
Runs a complete flow: trains the model and immediately classifies a test set
Good for end-to-end testing
STEP 16: Email Parser Script (parse_emails.py)
The parser script was used again to clean up the new code and csv files. 

STEP 17: Balanced Sample for Students (new_csv.py)
Produced a balanced sample. 

STEP 18: Build & Run Model (test_model.py)
Final training and testing step to evaluate model.


Notable Errors & Fixes

lxml install error	
Installed libxml2-dev libxslt1-dev
bs4 HTML parser error	
Switched to lxml
Virtualenv activation not working	
Used source myenv/bin/activate
File not found errors	
Used os.path.join + os.walk in parser
UTF-8 decoding issues	
Wrapped file opens in try/except, used errors='ignore'



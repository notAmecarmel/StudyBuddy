### README for StudyBuddy

---

## **Problem Statement**
In today's fast-paced academic environment, students often struggle to maintain an effective study routine and retain information. Current learning platforms lack personalized, efficient tools to help students organize their study materials, stay focused, and enhance their learning experience. The problem lies in the lack of intelligent tools that can break down complex topics into manageable chunks and motivate students to stay engaged with their studies.

---

## **Project Overview**
**StudyBuddy** is an AI-powered web application that transforms how students approach learning. By uploading PDF study materials, StudyBuddy processes the content into text, generates summaries, creates flashcards, and provides rapid-fire quizzes. With features like study schedules, to-do lists, Pomodoro timers, and motivational elements, StudyBuddy helps students organize their study sessions, stay motivated, and retain knowledge more efficiently. 

The application uses advanced Natural Language Processing (NLP) and Named Entity Recognition (NER) to analyze and convert documents into concise, useful study aids. Additionally, StudyBuddy motivates students by displaying random motivational quotes, changing background images, and tracking study streaks.

---

## **Tools & Technologies Used**

1. **Backend (Python):**
   - **Flask**: A micro web framework used to handle server-side logic and API requests.
   - **SpaCy**: A library for Natural Language Processing used to generate text summaries and process flashcards.
   - **PyPDF3**: For reading and extracting text from PDF documents.
   - **Random**: To fetch random motivational quotes and change background images.
   - **JSON**: Used to send and receive data between the frontend and backend.

2. **Frontend:**
   - **HTML, CSS, JavaScript**: For creating the user interface, ensuring responsiveness and interactivity.
   - **Flask Templates**: Used to render HTML files dynamically from the server.

3. **Machine Learning:**
   - **NLP and NER**: For text summarization and creating flashcards from extracted content.
   - **Heapq**: For optimizing data structures, particularly for rapid-fire quiz functionality.

---

## **How to Set Up the Project**

### **1. Clone the repository**
```bash
git clone https://github.com/yourusername/studybuddy.git
cd studybuddy
```

### **2. Set up a Virtual Environment**
It is recommended to create a virtual environment to manage dependencies.
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **3. Install the required dependencies**
Once the virtual environment is activated, install the necessary Python packages.
```bash
pip install -r requirements.txt
```

### **4. Set up your development environment**
Ensure that you have the following installed:
- Python 3.7+  
- Flask
- SpaCy  
- PyPDF3  
- Other required Python libraries listed in `requirements.txt`

### **5. Running the Project**
To start the Flask web server, use the following command:
```bash
python app.py
```
Your application will be accessible at `http://127.0.0.1:5000/` in your web browser.

### **6. Frontend Setup**
The frontend files (HTML, CSS, JavaScript) are located in the `templates` and `static` folders. No additional setup is needed for the frontend; it is served directly by Flask.

---

## **Commands to Run Your Project**
1. **Start the development server:**
   ```bash
   python app.py
   ```

2. **Run tests (if any):**
   ```bash
   pytest  # Assuming tests are implemented in the 'tests' directory
   ```

3. **Activate/deactivate virtual environment:**
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   deactivate
   ```

---

## **Contributing**
Feel free to fork the repository and make improvements. If you have any ideas, suggestions, or improvements, create a pull request, and we'll review it.

---

## **License**
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

By following these steps, you'll be able to set up StudyBuddy locally, experiment with its features, and contribute to its future development!

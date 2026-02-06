# Chemical Equipments' Analytics Visualizer ⚗️📊

![Project Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)
![Tech Stack](https://img.shields.io/badge/Stack-Full%20Stack-blue?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

A powerful hybrid application (Web & Desktop) designed to visualize, analyze, and report on chemical equipment parameters. This tool processes CSV data to provide real-time insights into Flowrate, Pressure, and Temperature metrics for industrial chemical equipment.

---

## 🌟 Key Features

* **📂 CSV Data Processing**: Seamlessly upload and parse bulk equipment data.
* **📈 Advanced Analytics**: Automated calculation of averages, total counts, and type distributions.
* **📊 Interactive Visualizations**:
    * **Web**: Dynamic Bar and Pie charts using `Chart.js`.
    * **Desktop**: Native plotting using `Matplotlib`.
* **📜 History Management**: Auto-saves and retrieves the last 5 uploaded datasets for comparison.
* **📄 PDF Reporting**: One-click generation of professional summary reports.
* **🌗 Dark/Light Mode**: Fully responsive UI with theme support (Web Version).
* **🔒 Secure & Scalable**: Built on Django REST Framework with basic authentication.

---

## 📸 Screenshots

### 🖥️ Web Dashboard (React)
> <img width="1214" height="951" alt="image" src="https://github.com/user-attachments/assets/60f6b61c-7184-4ed2-80e4-2a976c804d32" />

### 📄 PDF Report Output
> <img width="696" height="823" alt="image" src="https://github.com/user-attachments/assets/9b88005c-da4b-44a5-93dc-9ef09a4f968e" />


### 💻 Desktop Application (PyQt5)
> <img width="1919" height="1029" alt="image" src="https://github.com/user-attachments/assets/dab76371-a5ff-4a1e-93bf-7dd28997c2d6" />

---

## 🛠️ Tech Stack

### **Frontend (Web)**
* **Framework**: [React.js](https://react.dev/) + [Vite](https://vitejs.dev/)
* **Styling**: [Tailwind CSS](https://tailwindcss.com/) + Shadcn UI
* **Visualization**: Chart.js, React-Chartjs-2
* **Icons**: Lucide React

### **Frontend (Desktop)**
* **Framework**: PyQt5 (Python)
* **Visualization**: Matplotlib
* **Networking**: Requests

### **Backend**
* **Framework**: Django + Django REST Framework (DRF)
* **Data Processing**: Pandas
* **Reporting**: ReportLab (PDF Generation)
* **Database**: SQLite (Dev) / PostgreSQL (Prod ready)

---

## 🚀 Installation & Setup

Follow these steps to run the complete system locally.

### 1. Backend Setup (Django)

```bash
# Clone the repository
git clone [https://github.com/yourusername/chemical-visualizer.git](https://github.com/yourusername/chemical-visualizer.git)
cd chemical-visualizer/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start the server
python manage.py runserver

```

*Server runs at `http://127.0.0.1:8000`*

### 2. Frontend Web Setup (React)

```bash
# Navigate to frontend directory
cd ../frontend-react

# Install Node modules
npm install

# Start development server
npm run dev

```

*App runs at `http://localhost:5173`*

### 3. Frontend Desktop Setup (PyQt5)

```bash
# Navigate to desktop app directory
cd ../frontend-desktop

# Install desktop dependencies
pip install -r requirements.txt

# Run the application
python main.py

```

---

## 🔗 API Documentation

The backend provides the following RESTful endpoints:

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/api/upload/` | Upload CSV file and receive analysis stats. |
| `GET` | `/api/upload/` | Retrieve history of last 5 uploads. |
| `GET` | `/api/batch/<id>/` | Get detailed stats for a specific past batch. |
| `GET` | `/api/export-pdf/<id>/` | Download a PDF summary report for a batch. |

---

## 📂 Project Structure

```bash
chemical-visualizer/
├── backend/                 # Django Project
│   ├── core/                # Main App (Models, Views, Serializers)
│   ├── uploads/             # Media directory for CSVs
│   └── manage.py
├── frontend-react/          # Web Application
│   ├── src/
│   │   ├── components/      # UI Components (Charts, Cards)
│   │   └── pages/           # Dashboard & Layouts
│   └── vite.config.js
└── frontend-desktop/        # Desktop Application
    ├── ui/                  # PyQt5 UI Classes
    └── main.py              # Entry point

```

---

## 🧪 Sample Data

To test the application, use the provided `sample_equipment_data.csv` file located in the root directory. It contains the following columns:

* `Equipment Name`
* `Type` (Pump, Valve, Exchanger, Tank)
* `Flowrate` (m³/hr)
* `Pressure` (bar)
* `Temperature` (°C)

---

## 👨‍💻 Author

**Amritesh Kumar Rai**

* **Role**: Full Stack Developer
* **LinkedIn**: [[LinkedIn Profile](https://www.linkedin.com/in/amritesh-dev/)]
* **GitHub**: [@CodeVoyager3](https://github.com/CodeVoyager3)

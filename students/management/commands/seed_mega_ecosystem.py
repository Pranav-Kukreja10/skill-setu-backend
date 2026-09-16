import random
import time
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction
from django.contrib.auth.hashers import make_password
from django.db.models.signals import post_save

from accounts.models import User
from students.models import IndustrySector, JobBenchmark, StudentProfile, create_student_profile
from recruiters.models import Company, RecruiterProfile, JobListing
from recruiters.search import index_job_listing
from students.services import build_skills_matrix, generate_role_fit_matrix, compute_profile_strength

FIRST_NAMES_MALE = [
    "Aarav", "Aditya", "Rohan", "Siddharth", "Vikram", "Rahul", "Karan", "Abhishek",
    "Mayank", "Naveen", "Pranav", "Ishant", "Raghav", "Harsh", "Kunal", "Gaurav",
    "Tarun", "Nikhil", "Akash", "Varun", "Ayush", "Dev", "Ritwik", "Yash",
    "Shashank", "Aniket", "Manish", "Suraj", "Deepak", "Chirag", "Alok", "Kartik",
    "Tanmay", "Saurabh", "Vishal", "Sumit", "Praveen", "Rishi", "Gautam", "Arnav"
]

FIRST_NAMES_FEMALE = [
    "Ananya", "Sneha", "Pooja", "Priya", "Ishita", "Riya", "Kavya", "Tanvi",
    "Divya", "Meera", "Shreya", "Neha", "Simran", "Aishwarya", "Aditi", "Pallavi",
    "Swati", "Bhavna", "Anjali", "Sanskriti", "Roshni", "Deepika", "Kritika", "Preeti",
    "Sakshi", "Nandini", "Shruti", "Siddhi", "Vandana", "Akanksha", "Archana", "Garima"
]

LAST_NAMES = [
    "Sharma", "Verma", "Gupta", "Patel", "Reddy", "Nair", "Iyer", "Kashyap",
    "Bhatia", "Malhotra", "Mehra", "Singh", "Chauhan", "Rao", "Joshi", "Das",
    "Mukherjee", "Banerjee", "Saxena", "Kapoor", "Pillai", "Choudhary", "Dubey",
    "Mishra", "Trivedi", "Deshmukh", "Kulkarni", "Patil", "Agarwal", "Bansal", "Garg"
]

INSTITUTIONS = [
    "Indian Institute of Technology, Bombay",
    "Indian Institute of Technology, Delhi",
    "Indian Institute of Technology, Madras",
    "Indian Institute of Technology, Kharagpur",
    "Indian Institute of Technology, Roorkee",
    "National Institute of Technology, Karnataka",
    "National Institute of Technology, Trichy",
    "National Institute of Technology, Warangal",
    "Birla Institute of Technology and Science, Pilani",
    "Delhi Technological University",
    "Netaji Subhas University of Technology",
    "Vellore Institute of Technology, Vellore",
    "Thapar Institute of Engineering and Technology",
    "Chitkara University, Punjab",
    "PSG College of Technology, Coimbatore",
    "College of Engineering, Pune",
    "Jadavpur University, Kolkata",
    "Manipal Institute of Technology",
    "SRM Institute of Science and Technology",
    "RV College of Engineering, Bengaluru"
]

ENGINEERING_DISCIPLINES = {
    "Computer Science & Engineering": {
        "short": "CSE",
        "weight": 35,
        "target_roles": [
            "Backend Engineer", "Full Stack Engineer", "Software Development Engineer",
            "Cloud DevOps Engineer", "Systems Engineer", "Site Reliability Engineer"
        ],
        "skill_pools": {
            "technical": ["python", "java", "c++", "golang", "sql", "postgresql", "redis", "mongodb", "rest api", "graphql"],
            "frameworks": ["django", "fastapi", "spring boot", "express", "next.js", "react", "node.js"],
            "tools": ["docker", "kubernetes", "git", "linux", "aws", "postman", "jenkins", "terraform"],
            "soft": ["Problem Solving", "System Architecture", "Agile", "Team Collaboration", "Code Review"]
        },
        "project_templates": [
            ("Distributed Microservice Engine", ["Python", "FastAPI", "PostgreSQL", "Docker", "Redis"], "Engineered a high-throughput microservices backend handling 50k requests/min with Redis caching and JWT authentication."),
            ("Real-Time Collaborative Code Editor", ["React", "Node.js", "WebSockets", "MongoDB"], "Built an in-browser concurrent collaborative development environment with WebSockets and OT algorithms."),
            ("Cloud-Native CI/CD Pipeline & Ingress", ["Kubernetes", "Docker", "Terraform", "AWS"], "Designed a zero-downtime blue-green deployment pipeline with automated unit testing and Helm charts."),
            ("High-Performance Key-Value Store", ["C++", "Linux", "gRPC"], "Implemented an LSM-tree based persistent storage engine with write-ahead logging and thread pooling.")
        ],
        "certifications": [
            {"name": "AWS Certified Solutions Architect", "issuer": "Amazon Web Services", "skills_covered": ["aws", "cloud", "docker"]},
            {"name": "CKA: Certified Kubernetes Administrator", "issuer": "Linux Foundation", "skills_covered": ["kubernetes", "docker", "linux"]},
            {"name": "Oracle Certified Professional: Java SE", "issuer": "Oracle", "skills_covered": ["java", "spring boot"]}
        ]
    },
    "Artificial Intelligence & Data Science": {
        "short": "AI/DS",
        "weight": 20,
        "target_roles": [
            "Machine Learning Engineer", "Data Scientist", "AI Research Engineer",
            "NLP Engineer", "Computer Vision Specialist", "Data Engineer"
        ],
        "skill_pools": {
            "technical": ["python", "pytorch", "tensorflow", "scikit-learn", "sql", "pandas", "numpy", "r"],
            "frameworks": ["huggingface", "opencv", "langchain", "spark", "fastapi", "mlflow"],
            "tools": ["jupyter", "git", "docker", "dvc", "wandb", "aws sagemaker", "tableau"],
            "soft": ["Statistical Rigor", "Experimental Design", "Data Storytelling", "Analytical Thinking"]
        },
        "project_templates": [
            ("Autonomous Vision Perception Pipeline", ["Python", "PyTorch", "OpenCV", "CUDA"], "Trained a real-time object detection and segmentation network achieving 91% mAP on benchmark datasets."),
            ("Enterprise Semantic Search & RAG Agent", ["Python", "LangChain", "HuggingFace", "FastAPI"], "Developed a multi-document RAG pipeline using dense vector embeddings and cross-encoder re-ranking."),
            ("Distributed Big Data Analytics Engine", ["PySpark", "Apache Spark", "SQL", "AWS S3"], "Processed 500GB+ clickstream telemetry datasets with distributed Spark SQL queries and MLlib."),
            ("Algorithmic Market Sentiment Predictor", ["Python", "Scikit-Learn", "Pandas", "NLP"], "Extracted financial sentiment from news feeds to forecast equity volatility using ensemble trees.")
        ],
        "certifications": [
            {"name": "Deep Learning Specialization", "issuer": "DeepLearning.AI", "skills_covered": ["pytorch", "tensorflow", "python"]},
            {"name": "TensorFlow Developer Certificate", "issuer": "Google", "skills_covered": ["tensorflow", "python"]},
            {"name": "Databricks Certified Data Engineer", "issuer": "Databricks", "skills_covered": ["spark", "sql", "python"]}
        ]
    },
    "Electronics & Communication Engineering": {
        "short": "ECE",
        "weight": 18,
        "target_roles": [
            "VLSI Design Engineer", "Embedded Systems Engineer", "Firmware Engineer",
            "IoT Solutions Architect", "RF & Wireless Systems Engineer", "FPGA Design Engineer"
        ],
        "skill_pools": {
            "technical": ["verilog", "systemverilog", "embedded c", "c++", "vhdl", "matlab", "arm cortex", "i2c/spi/uart"],
            "frameworks": ["rtos", "freertos", "pcb design", "asic flow", "fpga synthesis"],
            "tools": ["cadence virtuoso", "xilinx vivado", "synopsys dc", "kicad", "keil uvision", "logic analyzer", "oscilloscope"],
            "soft": ["Hardware Debugging", "Low-Power Optimization", "Timing Closure", "Cross-Functional Collaboration"]
        },
        "project_templates": [
            ("RISC-V 32-bit Pipelined Processor Core", ["Verilog", "Xilinx Vivado", "FPGA"], "Implemented a 5-stage pipelined RISC-V CPU core with hazard detection, branch prediction, and synthesis on FPGA."),
            ("Industrial IoT Edge Gateway with FreeRTOS", ["Embedded C", "FreeRTOS", "ESP32", "MQTT"], "Architected a low-power wireless sensor hub with encrypted TLS telemetry to cloud broker."),
            ("Multi-Layer High-Speed PCB for Motor Drive", ["KiCad", "Altium Designer", "Signal Integrity"], "Designed a 4-layer PCB with impedance matching, thermal reliefs, and EMC compliance for BLDC motors."),
            ("Digital Signal Filter Accelerator on FPGA", ["SystemVerilog", "MATLAB", "DSP"], "Modeled FIR/IIR filter coefficients in MATLAB and mapped them to pipelined FPGA DSP slices.")
        ],
        "certifications": [
            {"name": "Certified Embedded Systems Professional", "issuer": "ARM Education", "skills_covered": ["embedded c", "arm cortex", "rtos"]},
            {"name": "VLSI Front-End Design & Verification", "issuer": "IEEE CEDA", "skills_covered": ["systemverilog", "verilog", "fpga"]},
            {"name": "IoT Foundations & Wireless Protocols", "issuer": "Cisco Networking Academy", "skills_covered": ["i2c/spi/uart", "embedded c"]}
        ]
    },
    "Mechanical & Mechatronics Engineering": {
        "short": "MECH",
        "weight": 12,
        "target_roles": [
            "Mechanical Design Engineer", "CAD/CAE Simulation Engineer", "Robotics Systems Engineer",
            "Thermal Systems Engineer", "Automotive Powertrain Analyst", "Manufacturing Automation Engineer"
        ],
        "skill_pools": {
            "technical": ["solidworks", "catia", "ansys", "fea", "cfd", "gd&t", "thermodynamics", "kinematics", "matlab"],
            "frameworks": ["dfm/dfa", "six sigma", "failure mode analysis (fmea)", "lean manufacturing"],
            "tools": ["autocad", "ansys workbench", "creo", "fusion 360", "abaqus", "3d printing", "cnc machining"],
            "soft": ["Design for Manufacturability", "Root Cause Analysis", "Project Engineering", "Vendor Coordination"]
        },
        "project_templates": [
            ("EV Battery Pack Thermal Management System", ["ANSYS Fluent", "CFD", "SolidWorks"], "Simulated liquid cooling channel geometry for 48V li-ion battery packs, reducing peak cell temperatures by 8°C."),
            ("6-DOF Robotic Arm Structural Optimization", ["SolidWorks", "ANSYS FEA", "Kinematics"], "Conducted structural FEA topology optimization, reducing robotic manipulator mass by 22% while maintaining stiffness."),
            ("Autonomous Mobile Robot (AMR) Drive Chassis", ["Fusion 360", "ROS", "Mechatronics"], "Designed a differential drive chassis with compliant suspension for warehouse navigation payloads up to 100kg."),
            ("Aerodynamic Drag Reduction for Commercial Trailer", ["CFD", "Catia V5", "Wind Tunnel Testing"], "Engineered rear aerodynamic fairings resulting in an 11% reduction in vehicle aerodynamic drag coefficient.")
        ],
        "certifications": [
            {"name": "CSWA: Certified SolidWorks Associate", "issuer": "Dassault Systèmes", "skills_covered": ["solidworks", "gd&t"]},
            {"name": "ANSYS Certified Simulation Specialist (FEA)", "issuer": "ANSYS Inc.", "skills_covered": ["ansys", "fea"]},
            {"name": "Six Sigma Green Belt", "issuer": "ASQ", "skills_covered": ["dfm/dfa", "six sigma"]}
        ]
    },
    "Electrical & Electronics Engineering": {
        "short": "EEE",
        "weight": 8,
        "target_roles": [
            "Power Systems Engineer", "Electrical Design Engineer", "EV Powertrain Engineer",
            "Control Systems Specialist", "Renewable Energy Integration Engineer", "PLC Automation Engineer"
        ],
        "skill_pools": {
            "technical": ["matlab/simulink", "power electronics", "plc programming", "scada", "motor drives", "grid integration", "circuit analysis"],
            "frameworks": ["ieee 1547 standards", "bms architecture", "industrial automation"],
            "tools": ["etap", "simulink", "autocad electrical", "pscad", "siemens tia portal", "multisim"],
            "soft": ["Electrical Safety Compliance", "Field Troubleshooting", "Substation Operations", "Technical Documentation"]
        },
        "project_templates": [
            ("Bidirectional EV On-Board Charger Converter", ["Simulink", "Power Electronics", "MATLAB"], "Simulated a 7.2kW dual-active bridge DC-DC converter with 96.5% efficiency and power factor correction."),
            ("Automated Factory PLC & SCADA Supervisory System", ["Siemens TIA Portal", "PLC Programming", "SCADA"], "Programmed ladder logic routines for an automated bottle filling line with real-time fault alarms."),
            ("Microgrid Energy Storage & Solar Inverter Control", ["ETAP", "Power Systems", "Grid Integration"], "Engineered islanding protection and frequency droop control for a 500kW rooftop PV microgrid installation."),
            ("BLDC Motor Vector Control (FOC) Driver", ["Simulink", "Motor Drives", "DSP"], "Implemented sensorless field-oriented control algorithms with space-vector PWM for electric two-wheelers.")
        ],
        "certifications": [
            {"name": "Certified Automation Engineer (PLC/SCADA)", "issuer": "Schneider Electric", "skills_covered": ["plc programming", "scada"]},
            {"name": "ETAP Certified Power System Analyst", "issuer": "ETAP", "skills_covered": ["etap", "power systems"]},
            {"name": "Electric Vehicle Technology Certification", "issuer": "SAE International", "skills_covered": ["power electronics", "motor drives"]}
        ]
    },
    "Civil & Structural Engineering": {
        "short": "CIVIL",
        "weight": 7,
        "target_roles": [
            "Structural Design Engineer", "BIM Coordinator", "Transportation Planning Engineer",
            "Geotechnical Engineer", "Construction Project Manager", "Surveying & GIS Specialist"
        ],
        "skill_pools": {
            "technical": ["structural analysis", "autocad", "staad.pro", "revit", "etabs", "concrete design", "steel structures", "gis/qgis"],
            "frameworks": ["is 456 / is 800 standards", "bim level 2", "nbc 2016", "leed green building"],
            "tools": ["autocad", "staad.pro", "etabs", "revit bim", "primavera p6", "qgis", "total station"],
            "soft": ["Site Supervision", "Structural Safety Auditing", "Contract Administration", "BOQ Estimation"]
        },
        "project_templates": [
            ("Seismic Analysis of Multi-Storey RCC Structure (G+12)", ["STAAD.Pro", "ETABS", "IS 1893 Standards"], "Carried out response spectrum dynamic analysis and ductile detailing for a 12-storey commercial tower."),
            ("BIM 4D Scheduling & Clash Detection Model", ["Revit", "Autodesk Navisworks", "Primavera P6"], "Coordinated multi-disciplinary MEP and structural models, eliminating 140+ construction site clashes."),
            ("Highway Geometric Alignment & Pavement Design", ["AutoCAD Civil 3D", "IRC Standards", "Transportation"], "Designed a 15km 4-lane bypass corridor including horizontal curves, drainage swales, and flexible pavement."),
            ("Soil Bearing Capacity & Deep Pile Foundation Model", ["GeoStudio", "Geotechnical", "Concrete Design"], "Analyzed soil liquefaction risk and designed driven RCC friction piles for riverfront floodplains.")
        ],
        "certifications": [
            {"name": "Autodesk Certified Professional: Revit for Structures", "issuer": "Autodesk", "skills_covered": ["revit", "autocad"]},
            {"name": "STAAD.Pro Certified Structural Engineer", "issuer": "Bentley Systems", "skills_covered": ["staad.pro", "structural analysis"]},
            {"name": "Project Management Professional (PMP)", "issuer": "PMI", "skills_covered": ["primavera p6"]}
        ]
    }
}

COMPANIES_DATA = [
    {"name": "Google India", "industry": "Information Technology", "reg": "CIN-U72900KA2003PTC033028", "hq": "Bengaluru, Karnataka", "web": "https://careers.google.com"},
    {"name": "Microsoft India", "industry": "Information Technology", "reg": "CIN-U72200DL1990PTC041040", "hq": "Hyderabad, Telangana", "web": "https://careers.microsoft.com"},
    {"name": "Amazon India", "industry": "Information Technology", "reg": "CIN-U74999KA2012PTC063251", "hq": "Bengaluru, Karnataka", "web": "https://amazon.jobs"},
    {"name": "Tata Consultancy Services", "industry": "Information Technology", "reg": "CIN-L22210MH1995PLC084781", "hq": "Mumbai, Maharashtra", "web": "https://tcs.com/careers"},
    {"name": "Infosys", "industry": "Information Technology", "reg": "CIN-L85110KA1981PLC013115", "hq": "Bengaluru, Karnataka", "web": "https://infosys.com/careers"},
    {"name": "Wipro Technologies", "industry": "Information Technology", "reg": "CIN-L32102KA1945PLC020800", "hq": "Bengaluru, Karnataka", "web": "https://wipro.com/careers"},
    {"name": "Cisco Systems India", "industry": "Information Technology", "reg": "CIN-U31909KA1995PTC019505", "hq": "Bengaluru, Karnataka", "web": "https://jobs.cisco.com"},
    {"name": "Adobe Systems India", "industry": "Information Technology", "reg": "CIN-U72200DL1997PTC085375", "hq": "Noida, Uttar Pradesh", "web": "https://adobe.com/careers"},
    {"name": "Oracle India", "industry": "Information Technology", "reg": "CIN-U72200KA1989PTC014272", "hq": "Bengaluru, Karnataka", "web": "https://oracle.com/careers"},
    {"name": "Atlassian India", "industry": "Information Technology", "reg": "CIN-U72900KA2018FTC111326", "hq": "Bengaluru, Karnataka", "web": "https://atlassian.com/company/careers"},

    {"name": "Texas Instruments India", "industry": "Electronics & Semiconductor", "reg": "CIN-U32109KA1985PTC006981", "hq": "Bengaluru, Karnataka", "web": "https://careers.ti.com"},
    {"name": "Intel Technology India", "industry": "Electronics & Semiconductor", "reg": "CIN-U72900KA1997PTC023080", "hq": "Bengaluru, Karnataka", "web": "https://intel.com/jobs"},
    {"name": "Qualcomm India", "industry": "Electronics & Semiconductor", "reg": "CIN-U72900DL1996PTC077759", "hq": "Hyderabad, Telangana", "web": "https://qualcomm.com/company/careers"},
    {"name": "NVIDIA Graphics India", "industry": "Electronics & Semiconductor", "reg": "CIN-U72200PN2004PTC019808", "hq": "Pune, Maharashtra", "web": "https://nvidia.com/careers"},
    {"name": "Synopsys India", "industry": "Electronics & Semiconductor", "reg": "CIN-U72200KA1995PTC018151", "hq": "Bengaluru, Karnataka", "web": "https://synopsys.com/careers"},

    {"name": "Tata Motors", "industry": "Mechanical Engineering", "reg": "CIN-L28920MH1945PLC004520", "hq": "Mumbai, Maharashtra", "web": "https://tatamotors.com"},
    {"name": "Mahindra & Mahindra", "industry": "Mechanical Engineering", "reg": "CIN-L65990MH1945PLC004558", "hq": "Mumbai, Maharashtra", "web": "https://mahindra.com/careers"},
    {"name": "Ather Energy", "industry": "Mechanical Engineering", "reg": "CIN-U40100KA2013PTC093769", "hq": "Bengaluru, Karnataka", "web": "https://atherenergy.com/careers"},
    {"name": "Ola Electric Mobility", "industry": "Mechanical Engineering", "reg": "CIN-U74999KA2017PLC125026", "hq": "Bengaluru, Karnataka", "web": "https://olaelectric.com/careers"},
    {"name": "Bosch India", "industry": "Mechanical Engineering", "reg": "CIN-L85110KA1951PLC000761", "hq": "Bengaluru, Karnataka", "web": "https://bosch.in/careers"},
    {"name": "Bajaj Auto", "industry": "Mechanical Engineering", "reg": "CIN-L65993PN2007PLC130076", "hq": "Pune, Maharashtra", "web": "https://bajajauto.com/careers"},

    {"name": "Larsen & Toubro", "industry": "Civil Engineering & Construction", "reg": "CIN-L99999MH1946PLC004768", "hq": "Mumbai, Maharashtra", "web": "https://larsentoubro.com"},
    {"name": "Tata Projects", "industry": "Civil Engineering & Construction", "reg": "CIN-U45203TG1979PLC057431", "hq": "Hyderabad, Telangana", "web": "https://tataprojects.com/careers"},
    {"name": "Afcons Infrastructure", "industry": "Civil Engineering & Construction", "reg": "CIN-U45200MH1976PLC019335", "hq": "Mumbai, Maharashtra", "web": "https://afcons.com/careers"},
    {"name": "GMR Group", "industry": "Civil Engineering & Construction", "reg": "CIN-L45203MH1996PLC281138", "hq": "New Delhi, Delhi", "web": "https://gmrgroup.in/careers"},

    {"name": "Schneider Electric India", "industry": "Electrical & Electronics Engineering", "reg": "CIN-U31909DL1995PTC068948", "hq": "Gurugram, Haryana", "web": "https://se.com/careers"},
    {"name": "Siemens India", "industry": "Electrical & Electronics Engineering", "reg": "CIN-L28920MH1957PLC010839", "hq": "Mumbai, Maharashtra", "web": "https://siemens.com/careers"},
    {"name": "ABB India", "industry": "Electrical & Electronics Engineering", "reg": "CIN-L32202KA1949PLC032923", "hq": "Bengaluru, Karnataka", "web": "https://abb.com/careers"},
    {"name": "Havells India", "industry": "Electrical & Electronics Engineering", "reg": "CIN-L31900DL1983PLC016304", "hq": "Noida, Uttar Pradesh", "web": "https://havells.com/careers"},

    {"name": "Zerodha Broking", "industry": "Finance & Commerce", "reg": "CIN-U65990KA2018PTC116578", "hq": "Bengaluru, Karnataka", "web": "https://zerodha.com"},
    {"name": "Morgan Stanley", "industry": "Finance & Commerce", "reg": "CIN-U67120MH1993FTC072704", "hq": "Mumbai, Maharashtra", "web": "https://morganstanley.com/careers"},
    {"name": "PhonePe", "industry": "Finance & Commerce", "reg": "CIN-U67190KA2012PTC176030", "hq": "Bengaluru, Karnataka", "web": "https://phonepe.com/careers"}
]

JOB_TEMPLATES = [
    {"title": "Junior Backend Systems Engineer", "disc": "CSE", "role_type": "FULL_TIME", "ctc": "14 - 18 LPA", "loc": "Bengaluru (Hybrid)", "remote": False, "skills": ["python", "django", "postgresql", "rest api", "docker"]},
    {"title": "Full Stack Software Developer", "disc": "CSE", "role_type": "FULL_TIME", "ctc": "12 - 16 LPA", "loc": "Hyderabad", "remote": False, "skills": ["react", "node.js", "next.js", "sql", "typescript"]},
    {"title": "Cloud DevOps & Platform Intern", "disc": "CSE", "role_type": "INTERNSHIP", "ctc": "INR 45,000/month", "loc": "Remote", "remote": True, "skills": ["docker", "kubernetes", "linux", "aws", "git"]},
    {"title": "Systems Software Development Engineer", "disc": "CSE", "role_type": "FULL_TIME", "ctc": "18 - 24 LPA", "loc": "Bengaluru", "remote": False, "skills": ["c++", "linux", "python", "docker", "git"]},
    {"title": "Distributed Database Engineering Intern", "disc": "CSE", "role_type": "INTERNSHIP", "ctc": "INR 50,000/month", "loc": "Pune", "remote": False, "skills": ["c++", "postgresql", "linux", "redis"]},
    {"title": "Site Reliability & Ingress Engineer", "disc": "CSE", "role_type": "FULL_TIME", "ctc": "15 - 20 LPA", "loc": "Bengaluru", "remote": True, "skills": ["kubernetes", "docker", "terraform", "linux", "golang"]},

    {"title": "Machine Learning Engineer (Core)", "disc": "AI/DS", "role_type": "FULL_TIME", "ctc": "16 - 22 LPA", "loc": "Bengaluru", "remote": False, "skills": ["python", "pytorch", "tensorflow", "scikit-learn", "sql"]},
    {"title": "NLP & Generative AI Research Intern", "disc": "AI/DS", "role_type": "INTERNSHIP", "ctc": "INR 60,000/month", "loc": "Hyderabad (Hybrid)", "remote": False, "skills": ["python", "pytorch", "huggingface", "langchain"]},
    {"title": "Computer Vision Algorithm Specialist", "disc": "AI/DS", "role_type": "FULL_TIME", "ctc": "18 - 26 LPA", "loc": "Noida", "remote": False, "skills": ["python", "opencv", "pytorch", "docker"]},
    {"title": "Big Data Platforms & Spark Engineer", "disc": "AI/DS", "role_type": "FULL_TIME", "ctc": "14 - 19 LPA", "loc": "Bengaluru", "remote": True, "skills": ["python", "spark", "sql", "aws", "pandas"]},

    {"title": "RTL Design & Verification Engineer", "disc": "ECE", "role_type": "FULL_TIME", "ctc": "15 - 22 LPA", "loc": "Bengaluru", "remote": False, "skills": ["verilog", "systemverilog", "fpga", "vhdl"]},
    {"title": "Embedded Firmware Engineer (ARM)", "disc": "ECE", "role_type": "FULL_TIME", "ctc": "10 - 15 LPA", "loc": "Hyderabad", "remote": False, "skills": ["embedded c", "arm cortex", "rtos", "i2c/spi/uart"]},
    {"title": "IoT Edge Hardware Development Intern", "disc": "ECE", "role_type": "INTERNSHIP", "ctc": "INR 35,000/month", "loc": "Bengaluru (Hybrid)", "remote": False, "skills": ["embedded c", "pcb design", "kicad", "freertos"]},
    {"title": "ASIC Physical Design & Timing Engineer", "disc": "ECE", "role_type": "FULL_TIME", "ctc": "18 - 25 LPA", "loc": "Noida", "remote": False, "skills": ["cadence virtuoso", "verilog", "synopsys dc"]},

    {"title": "EV Battery Pack Thermal Design Engineer", "disc": "MECH", "role_type": "FULL_TIME", "ctc": "11 - 16 LPA", "loc": "Bengaluru", "remote": False, "skills": ["solidworks", "ansys", "cfd", "thermodynamics"]},
    {"title": "Robotics Mechanical Simulation Intern", "disc": "MECH", "role_type": "INTERNSHIP", "ctc": "INR 40,000/month", "loc": "Pune", "remote": False, "skills": ["solidworks", "ansys", "fea", "gd&t"]},
    {"title": "Automotive CAD & CAE Crash Analyst", "disc": "MECH", "role_type": "FULL_TIME", "ctc": "12 - 17 LPA", "loc": "Chennai", "remote": False, "skills": ["catia", "ansys", "fea", "gd&t"]},
    {"title": "Manufacturing Automation & Tooling Engineer", "disc": "MECH", "role_type": "FULL_TIME", "ctc": "9 - 13 LPA", "loc": "Mumbai", "remote": False, "skills": ["autocad", "solidworks", "dfm/dfa", "six sigma"]},

    {"title": "EV Motor Drives & Inverter Engineer", "disc": "EEE", "role_type": "FULL_TIME", "ctc": "12 - 18 LPA", "loc": "Bengaluru", "remote": False, "skills": ["simulink", "power electronics", "matlab", "motor drives"]},
    {"title": "Industrial PLC & SCADA Automation Specialist", "disc": "EEE", "role_type": "FULL_TIME", "ctc": "8 - 12 LPA", "loc": "Gurugram", "remote": False, "skills": ["plc programming", "scada", "siemens tia portal"]},
    {"title": "Renewable Microgrid Integration Intern", "disc": "EEE", "role_type": "INTERNSHIP", "ctc": "INR 30,000/month", "loc": "Noida (Hybrid)", "remote": False, "skills": ["etap", "power systems", "matlab", "grid integration"]},

    {"title": "Structural RCC & Steel Design Engineer", "disc": "CIVIL", "role_type": "FULL_TIME", "ctc": "8 - 12 LPA", "loc": "Mumbai", "remote": False, "skills": ["staad.pro", "etabs", "autocad", "concrete design"]},
    {"title": "BIM Modeling & Clash Coordination Intern", "disc": "CIVIL", "role_type": "INTERNSHIP", "ctc": "INR 28,000/month", "loc": "New Delhi", "remote": False, "skills": ["revit", "autocad", "primavera p6"]},
    {"title": "Transportation & Highway Corridor Engineer", "disc": "CIVIL", "role_type": "FULL_TIME", "ctc": "9 - 14 LPA", "loc": "Hyderabad", "remote": False, "skills": ["autocad", "staad.pro", "structural analysis"]}
]


class Command(BaseCommand):
    help = "Seeds 10,000 diverse engineering candidate profiles, 30+ companies, recruiters, and 100+ job listings"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("=== Starting Mega Ecosystem Expansion Seeder ==="))
        t_start = time.time()

        # Step 1: Ensure Industry Sectors exist
        self.stdout.write("[-] Validating / populating Industry Sectors...")
        sectors_map = {}
        for sector_name in [
            "Information Technology", "Artificial Intelligence & Machine Learning",
            "Electronics & Semiconductor", "Mechanical Engineering", "Electrical & Electronics Engineering",
            "Civil Engineering & Construction", "Finance & Commerce"
        ]:
            sec, _ = IndustrySector.objects.get_or_create(
                name=sector_name,
                defaults={"description": f"Domain covering {sector_name}"}
            )
            sectors_map[sector_name] = sec

        # Step 2: Seed Companies
        self.stdout.write("[-] Seeding 30+ Enterprise & Startup Companies...")
        companies = {}
        for cdata in COMPANIES_DATA:
            sec = sectors_map.get(cdata["industry"], sectors_map["Information Technology"])
            comp, created = Company.objects.update_or_create(
                name=cdata["name"],
                defaults={
                    "registration_number": cdata["reg"],
                    "is_verified": True,
                    "website": cdata["web"],
                    "industry": sec,
                    "branding_logo_url": f"https://www.google.com/s2/favicons?domain={cdata['web'].replace('https://', '').replace('http://', '').split('/')[0]}&sz=128",
                    "description": f"Pioneering technology leader in {cdata['industry']}, building hyperscale products.",
                    "headquarters": cdata["hq"]
                }
            )
            companies[comp.name] = comp

        # Step 3: Seed Recruiters
        self.stdout.write("[-] Seeding Recruiters for all companies...")
        recruiters = []
        default_pwd_hash = make_password("password123")

        # Disconnect post_save to avoid auto-creating student profiles for recruiters
        post_save.disconnect(create_student_profile, sender=User)

        for comp_name, comp in companies.items():
            comp_slug = comp_name.lower().replace(" ", "_").replace("&", "and").replace(",", "").replace(".", "")[:15]
            rec_username = f"hr_{comp_slug}"
            rec_email = f"talent@{comp_slug}.example.com"
            
            u, u_created = User.objects.get_or_create(
                username=rec_username,
                defaults={
                    "email": rec_email,
                    "role": User.Role.RECRUITER,
                    "first_name": comp_name.split()[0],
                    "last_name": "HR Lead",
                    "password": default_pwd_hash
                }
            )
            if u_created:
                u.set_password("password123")
                u.save()

            rp, _ = RecruiterProfile.objects.update_or_create(
                user=u,
                defaults={
                    "company": comp,
                    "designation": "Head of University Relations & Technical Talent",
                    "department": "Campus Talent Acquisition",
                    "is_company_admin": True,
                    "contact_phone": "+91 98765 00000",
                    "location": comp.headquarters
                }
            )
            recruiters.append(rp)

        # Step 4: Seed Job Listings
        self.stdout.write("[-] Seeding 100+ rich Job Listings across engineering domains...")
        created_listings = 0
        listing_objs = []
        
        # Multiply templates across companies to reach 100+ listings
        for idx, template in enumerate(JOB_TEMPLATES):
            for comp_idx, (comp_name, comp) in enumerate(list(companies.items())[:5]):
                rec = comp.recruiters.first()
                if not rec:
                    continue
                
                title = f"{template['title']} - {comp.name.split()[0]} Campus Drive"
                deadline = timezone.now() + timedelta(days=random.randint(15, 60))
                
                # Check if listing already exists
                existing = JobListing.objects.filter(title=title, company=comp).first()
                if existing:
                    continue

                jl = JobListing(
                    company=comp,
                    recruiter=rec,
                    title=title,
                    role_type=template["role_type"],
                    target_audience=JobListing.TargetAudience.STUDENT,
                    status=JobListing.ListingStatus.PUBLISHED,
                    stipend_or_ctc=template["ctc"],
                    location=template["loc"],
                    is_remote=template["remote"],
                    application_deadline=deadline,
                    tenure="Permanent" if template["role_type"] == "FULL_TIME" else "6 Months",
                    open_positions=random.randint(2, 10),
                    required_skills=template["skills"],
                    eligibility_criteria={"min_cgpa": round(random.uniform(6.5, 7.5), 1), "min_nheqf": "LEVEL_6_0"},
                    description=(
                        f"We are hiring a high-caliber {template['title']} at {comp.name}. "
                        f"You will collaborate on critical infrastructure, scale production systems, "
                        f"and push technological boundaries. Requirements: Proficiency in {', '.join(template['skills'])}."
                    ),
                    is_diversity_drive=random.choice([True, False, False]),
                    target_gender="ALL"
                )
                listing_objs.append(jl)

        JobListing.objects.bulk_create(listing_objs, batch_size=200)
        self.stdout.write(f"  [+] Bulk created {len(listing_objs)} job listings.")

        # Index created job listings
        self.stdout.write("[-] Indexing job listings search corpus & embeddings...")
        all_unindexed_listings = JobListing.objects.filter(search_corpus='').select_related("company")
        indexed_count = 0
        for jl in all_unindexed_listings:
            try:
                index_job_listing(jl)
                indexed_count += 1
            except Exception as e:
                pass
        self.stdout.write(f"  [+] Indexed {indexed_count} job listings.")

        # Step 5: Pre-compute JobBenchmarks dictionary in memory for ultra-fast role fitment
        self.stdout.write("[-] Loading job benchmarks in memory for instant fitment scoring...")
        benchmarks = list(JobBenchmark.objects.select_related("sector").all())
        benchmarks_by_title = {b.role_title: b for b in benchmarks}

        # Step 6: Generate 10,000 Diverse Engineering Student Accounts in Fast Batches
        TARGET_STUDENTS = 10000
        existing_student_count = StudentProfile.objects.count()
        self.stdout.write(f"[-] Current student profiles in DB: {existing_student_count}")
        self.stdout.write(f"[-] Generating {TARGET_STUDENTS} new engineering student accounts...")

        BATCH_SIZE = 1000
        disciplines_list = list(ENGINEERING_DISCIPLINES.keys())
        disciplines_weights = [ENGINEERING_DISCIPLINES[d]["weight"] for d in disciplines_list]

        # Calculate offset so usernames are strictly unique
        base_id_offset = int(time.time()) % 100000

        total_created = 0
        for batch_num in range(0, TARGET_STUDENTS, BATCH_SIZE):
            b_start = time.time()
            current_batch_size = min(BATCH_SIZE, TARGET_STUDENTS - batch_num)
            
            user_batch = []
            profile_batch_data = []

            for i in range(current_batch_size):
                student_idx = batch_num + i + 1
                unique_tag = f"{base_id_offset}_{student_idx}"

                # Gender & Name
                is_female = random.random() < 0.35
                gender = StudentProfile.Gender.FEMALE if is_female else StudentProfile.Gender.MALE
                first_name = random.choice(FIRST_NAMES_FEMALE if is_female else FIRST_NAMES_MALE)
                last_name = random.choice(LAST_NAMES)
                username = f"{first_name.lower()}_{last_name.lower()}_{unique_tag}"
                email = f"{first_name.lower()}.{last_name.lower()}.{unique_tag}@campus.edu"

                user = User(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    role=User.Role.STUDENT,
                    password=default_pwd_hash
                )
                user_batch.append(user)

                # Discipline & Academic Specs
                discipline_name = random.choices(disciplines_list, weights=disciplines_weights)[0]
                disc_info = ENGINEERING_DISCIPLINES[discipline_name]
                institution = random.choice(INSTITUTIONS)
                degree = random.choice(["B.Tech", "B.Tech (Honours)", "M.Tech", "B.E."])
                cgpa = round(random.uniform(6.2, 9.7), 2)
                grad_year = random.choice([2024, 2025, 2026, 2027])
                nheqf = "LEVEL_7_0" if "M.Tech" in degree else "LEVEL_6_0"

                # Skills Matrix Generation
                num_tech = random.randint(4, 7)
                num_frame = random.randint(2, 4)
                num_tools = random.randint(2, 4)
                num_soft = random.randint(2, 4)

                selected_tech = random.sample(disc_info["skill_pools"]["technical"], min(num_tech, len(disc_info["skill_pools"]["technical"])))
                selected_frame = random.sample(disc_info["skill_pools"]["frameworks"], min(num_frame, len(disc_info["skill_pools"]["frameworks"])))
                selected_tools = random.sample(disc_info["skill_pools"]["tools"], min(num_tools, len(disc_info["skill_pools"]["tools"])))
                selected_soft = random.sample(disc_info["skill_pools"]["soft"], min(num_soft, len(disc_info["skill_pools"]["soft"])))

                all_extracted_skills = []
                for s in selected_tech + selected_frame + selected_tools:
                    pe = random.randint(65, 95)
                    er = random.randint(60, 90)
                    all_extracted_skills.append({
                        "name": s,
                        "project_evidence_score": pe,
                        "experience_recency_score": er
                    })

                # Certifications
                has_certs = random.random() < 0.65
                candidate_certs = []
                if has_certs:
                    cert_sample = random.sample(disc_info["certifications"], random.randint(1, min(2, len(disc_info["certifications"]))))
                    for cs in cert_sample:
                        candidate_certs.append({
                            "name": cs["name"],
                            "issuer": cs["issuer"],
                            "issue_year": random.choice([2023, 2024, 2025]),
                            "credential_url": f"https://verify.credentials.example/{unique_tag}",
                            "skills_covered": cs["skills_covered"]
                        })

                # Build Skills Matrix (Ws = 0.6*Pe + 0.4*Er with +15% credential boost)
                skills_matrix = build_skills_matrix(
                    extracted_skills_list=all_extracted_skills,
                    certifications=candidate_certs
                )

                # Projects
                num_proj = random.randint(1, 3)
                proj_sample = random.sample(disc_info["project_templates"], min(num_proj, len(disc_info["project_templates"])))
                candidate_projects = []
                for pt, ptech, pdesc in proj_sample:
                    candidate_projects.append({
                        "title": pt,
                        "technologies": ptech,
                        "description": pdesc
                    })

                # Role Fitment Matrix (Against target roles)
                candidate_target_roles = random.sample(disc_info["target_roles"], random.randint(2, min(4, len(disc_info["target_roles"]))))
                role_fit_matrix = {}
                for tr in candidate_target_roles:
                    bm = benchmarks_by_title.get(tr)
                    sector_title = bm.sector.name if bm else discipline_name
                    # Calculate fast realistic fitment score
                    fit_score = random.randint(68, 94)
                    fit_level = "High Match" if fit_score >= 80 else "Medium Match"
                    role_fit_matrix[tr] = {
                        "score": fit_score,
                        "fit_level": fit_level,
                        "sector": sector_title,
                        "verified_confidence_score": fit_score if random.random() < 0.5 else None
                    }

                # Verification Status & Confidence Score
                is_verified = random.random() < 0.45
                if is_verified:
                    overall_confidence_score = round(random.uniform(70.0, 92.0), 1)
                else:
                    overall_confidence_score = 0.0

                # Calculate Profile Strength Score (P_overall)
                # S_cog (45%), S_proj (30%), S_cert (15%), S_acad (10%)
                weights = [v.get("weight", 0) for v in skills_matrix.values() if isinstance(v, dict)]
                mean_weight = sum(weights) / len(weights) if weights else 0.0
                cert_score = 100.0 if len(candidate_certs) >= 3 else (85.0 if len(candidate_certs) == 2 else (70.0 if len(candidate_certs) == 1 else 0.0))
                acad_score = min(100.0, cgpa * 10.0)
                profile_strength_score = round(
                    (0.45 * overall_confidence_score) +
                    (0.30 * mean_weight) +
                    (0.15 * cert_score) +
                    (0.10 * acad_score),
                    1
                )

                # Denormalized Search Corpus for text & keyword matching
                corpus_parts = [
                    f"Candidate: {first_name} {last_name} ({disc_info['short']} Engineer)",
                    f"Institution: {institution} | Department: {discipline_name} | Degree: {degree} | CGPA: {cgpa}",
                    f"Primary Skills: {', '.join(skills_matrix.keys())}",
                    f"Seeking Roles: {', '.join(candidate_target_roles)}",
                    f"Categorized Competencies: Technical: {', '.join(selected_tech)} | Frameworks: {', '.join(selected_frame)} | Tools: {', '.join(selected_tools)} | Soft: {', '.join(selected_soft)}",
                    f"Projects: {' '.join([p['title'] + ': ' + p['description'] for p in candidate_projects])}",
                    f"Certifications: {' '.join([c['name'] for c in candidate_certs])}"
                ]
                search_corpus = "\n".join(corpus_parts)

                profile_batch_data.append({
                    "gender": gender,
                    "skills_matrix": skills_matrix,
                    "projects": candidate_projects,
                    "role_fit_matrix": role_fit_matrix,
                    "target_roles": candidate_target_roles,
                    "raw_extracted_skills": list(skills_matrix.keys()),
                    "institution": institution,
                    "department": discipline_name,
                    "degree": degree,
                    "cgpa": cgpa,
                    "graduation_year": grad_year,
                    "nheqf_level": nheqf,
                    "skills_categorized": {
                        "technical_skills": selected_tech,
                        "frameworks": selected_frame,
                        "tools": selected_tools,
                        "soft_skills": selected_soft
                    },
                    "certifications": candidate_certs,
                    "overall_confidence_score": overall_confidence_score,
                    "profile_strength_score": profile_strength_score,
                    "is_verified": is_verified,
                    "placement_status": StudentProfile.PlacementStatus.UNPLACED,
                    "search_corpus": search_corpus,
                    "bio": f"Passionate {discipline_name} student at {institution} specializing in {', '.join(selected_tech[:3])}."
                })

            # Bulk insert users
            with transaction.atomic():
                created_users = User.objects.bulk_create(user_batch)
                
                # Pair with StudentProfiles
                student_profiles = []
                for u, pdata in zip(created_users, profile_batch_data):
                    sp = StudentProfile(user=u, **pdata)
                    student_profiles.append(sp)

                StudentProfile.objects.bulk_create(student_profiles)

            total_created += current_batch_size
            b_dur = time.time() - b_start
            self.stdout.write(f"  [+] Inserted batch {total_created}/{TARGET_STUDENTS} profiles ({current_batch_size} in {b_dur:.2f}s, {total_created*100/TARGET_STUDENTS:.0f}%)")

        # Reconnect post_save signal
        post_save.connect(create_student_profile, sender=User)

        t_total = time.time() - t_start
        self.stdout.write(self.style.SUCCESS(f"\n[DONE] Successfully expanded ecosystem in {t_total:.2f}s!"))
        self.stdout.write(self.style.SUCCESS(f"Total Users: {User.objects.count()}"))
        self.stdout.write(self.style.SUCCESS(f"Total Student Profiles: {StudentProfile.objects.count()}"))
        self.stdout.write(self.style.SUCCESS(f"Total Companies: {Company.objects.count()}"))
        self.stdout.write(self.style.SUCCESS(f"Total Recruiters: {RecruiterProfile.objects.count()}"))
        self.stdout.write(self.style.SUCCESS(f"Total Job Listings: {JobListing.objects.count()}"))

# 🏠🔌 **IoT Smart Home Project**  
🚀 **An intelligent, automated smart home system that reacts to real-time sensor data!**  

This project **integrates IoT devices and sensors** to simulate a smart home, where components interact dynamically to enhance **security, comfort, and automation**. It uses a **Raspberry Pi**, **ESP32 microcontroller**, and various sensors to **monitor, analyze, and react** to environmental conditions in real time.  

---

## 📂 **Project Repository**  
🔗 **GitHub Repository:** [Click here](https://github.com/christiankfoury/iot-project.git)  

---

## ⚡ **Getting Started**  
Follow these simple steps to deploy the project:  

1️⃣ **Upload the `ESP_Publish.ino` code** to the ESP32.  
2️⃣ **Run `DashboardFinal.py`** on the Raspberry Pi.  
3️⃣ **Open** `localhost:8050` in your browser to view the real-time dashboard.  

💡 **And just like that—your smart home is online!**  

---

## 🤖 **How It Works: Smart Home Automation in Action**  

### **1️⃣ Data Collection & Sensor Input (ESP32 as the Sensor Hub)**  
The **ESP32 microcontroller** continuously gathers **real-time environmental data** from various sensors:  
- 🌡️ **DHT11 Sensor:** Measures **temperature & humidity**.  
- 💡 **Photoresistor:** Detects **ambient light intensity**.  
- 📡 **RFID Scanner (RC522):** Reads **user ID tags for access control**.  
- 🔄 **DC Motor (Fan):** Used for **temperature-based cooling automation**.  
- The ESP32 **publishes sensor readings via MQTT**, making them available for the Raspberry Pi to process.  

---

### **2️⃣ Data Transmission & Processing (Raspberry Pi as the Brain)**  
- The **Raspberry Pi** acts as the **central hub**, subscribing to **MQTT topics** to receive **live sensor data**.  
- Once data is received, it is processed using **Python & Plotly**, and the system makes **intelligent automation decisions** based on predefined rules.  

📡 **Project Block Diagram:**  
![image](https://github.com/user-attachments/assets/93ef58e7-63f3-4032-8470-60f4397d95c7)  

---

### **3️⃣ Intelligent Automation & Smart Home Reactions**  
Once the **Raspberry Pi processes incoming data**, it triggers **various smart home actions**:  

✅ **RFID Security System:**  
- Users **scan their RFID tag** at the reader.  
- If **authorized**, access is **granted**.  
- If **unauthorized**, a warning is displayed on the dashboard.  

✅ **Adaptive Lighting Control:**  
- The **photoresistor measures light intensity**.  
- If the **room is dark**, the **LED light automatically turns ON**.  
- If the **room is bright**, the **LED light turns OFF**.  

### ✅ Smart Fan Control (Temperature-Based Automation)
- If the **temperature exceeds a threshold**, the system sends an **email notification** asking if the user wants to turn on the fan.  
- If the user **responds "YES"**, the **DC motor (fan) is activated**.  
- The fan **automatically turns off** once the temperature returns to normal.  

📧 **Email-Based Fan Activation Example:**  
When the temperature surpasses the threshold, the system automatically sends an email alert:  

![image](https://github.com/user-attachments/assets/f457ba11-ec83-48dc-8828-7839af4cf53a)  

The user can reply with **"yes"**, and the system will immediately turn on the fan to regulate the temperature.  


✅ **Real-Time Dashboard for User Monitoring:**  
- A **Plotly-powered web dashboard** displays:  
  - 📊 **Temperature & Humidity Readings**  
  - 💡 **Light Intensity Levels**  
  - 📡 **RFID Access Logs**  
  - 🌀 **Fan Activation Status**  

📡 **Final Project Overview:**  
![image](https://github.com/user-attachments/assets/b0097387-7552-4c04-bf57-793c23538e24)  

---

### **4️⃣ Web Dashboard & User Interaction**  
- The dashboard, built with **Plotly and Python**, allows users to:  
  - **Monitor real-time data** from all sensors.  
  - **Receive email alerts** for critical temperature conditions.  
  - **View RFID access logs and manage user profiles**.  
  - **Adjust thresholds and view fan activation status dynamically**.  


---

## 🛠️ **Software & Tools Used**  
💻 **Development & Debugging:**  
- 🐍 **Python (Backend Processing & Dashboard Logic)**  
- 📊 **Plotly (Graphing & Dashboard Visualization)**  
- 🔌 **Arduino IDE (ESP32 Code Deployment)**  
- 🎨 **CSS & Bootstrap (Dashboard Styling)**  
- 🌐 **Chromium (Dashboard Visualization)**  
- 🛠️ **Node-RED (MQTT Debugging & Data Flow Testing)**  

🌎 **Communication Protocols:**  
- 📡 **MQTT:** Enables **real-time data transmission** between the **ESP32 & Raspberry Pi**.  
- ✉️ **SMTP & IMAP:** Used for **sending & receiving email notifications**.  
- 🌍 **HTTP:** Ensures **smooth interaction** between the **web dashboard and backend**.  

---

## 🔩 **Hardware Components Used**  
👾 **IoT Devices & Sensors Integrated into the System:**  
- 🖥️ **Raspberry Pi 400**  
- 📡 **ESP32 NodeMCU**  
- 📶 **RC522 RFID Tag Reader + RFID Tags**  
- 💡 **Photoresistor (Light Sensor)**  
- 🌡️ **DHT11 (Temperature & Humidity Sensor)**  
- 🚀 **L293D Motor Driver + DC Fan**  
- 🔦 **LED Light**  
- 🔌 **10KΩ & 220Ω Resistors**  
- 🔗 **Female & Male Wire Connectors**  

📸 **Hardware Setup:**  
![image](https://github.com/user-attachments/assets/2258eecd-eabc-4d51-86d9-0c537d9494da)  

---

## 🚀 **Final Results & Smart Home Impact**  
✅ **Automated environment monitoring and response system**.  
✅ **RFID-based security for controlled access**.  
✅ **Email alerts for critical temperature conditions**.  
✅ **Real-time dashboard for live monitoring and interaction**.  
✅ **Seamless communication between IoT components using MQTT & HTTP**.  

---

# **🔹 Transforming Homes into Smart Spaces!**  
This project successfully **demonstrates the power of IoT in home automation**, integrating **real-time monitoring, automated control, and remote interaction** into a **seamless smart home system**.  

👨‍💻 **Ready to build your own smart home system?** Get started today! 🎯  

# StitchWitch

## **Inspiration**
The inspiration behind **StitchWitch** comes from the urgent need to address the alarming rate of surgical errors, which exceed 4,000 incidents annually. While human errors are unavoidable, we aim to leverage advanced AI technology to enhance surgical precision and patient safety, potentially impacting thousands of lives each year.

---

## **What It Does**
**StitchWitch** utilizes the Gemini Pro AI model, integrated with Ray-Ban smart glasses, to provide real-time assistance during surgeries. The system analyzes surgical procedures, detects potential errors, and offers immediate feedback to the surgical team, reducing mistakes and optimizing surgical outcomes.

---

## **How We Built It**

### **Frontend**
- Built using **Python** and the **Reflex** framework for streamlined development.
- **Reflex** eliminated the need for HTML, CSS, and JavaScript, enabling a robust application within a single framework.
- Implemented easy route management for a seamless user experience.

### **Backend**
- Leveraged the **Reflex** framework for backend logic.
- Utilized `yield` statements in event handlers to initiate state changes.
- Integrated **OpenCV** to extract frames from surgical videos for real-time analysis.

### **AI Pipeline**
We designed a multi-agent AI system to support surgical teams:
1. **Observer-Agent**: Observes live video frames, describes the scene in natural language, and provides outputs for other agents.
2. **Procedure-Agent**: Maintains a history of actions through a chat-based interface.
3. **Alert-Agent**: Uses few-shot prompting to recognize anatomy and standard procedures, alerting users of risks.
4. **Supervisor-Agent (Optional)**: Reviews procedure history to ensure all steps were followed accurately.

---

## **Challenges We Faced**
- **Gemini Constraints**:
  - Inability to fine-tune Gemini on video data or conduct multi-turn conversations with its vision model.
  - Difficulty navigating safety controls and adapting the AI for surgical use cases.
- **Hardware Limitations**:
  - Lack of access to smart glasses required simulation of a surgery live stream using OpenCV.
- **Processing Delays**:
  - Managing backend processing times to ensure near-instant feedback during simulations.

---

## **Accomplishments**
- Achieved multimodal few-shot prompting of vision-language models for domain-specific problems.
- Simulated a live surgery stream with real-time video analysis using **OpenCV** and **Gemini**.
- Successfully implemented the Reflex framework for full-stack development, enhancing our technical expertise.

---

## **What We Learned**
This project deepened our understanding of AI deployment and computer vision in healthcare. We navigated complex safety protocols and discovered the potential of prompt engineering for solving medical challenges. This experience underscored the importance of interdisciplinary collaboration in advancing healthcare innovation.

---

## **What’s Next for StitchWitch**
- **Data Collection**: Enhance datasets for fine-tuning and model prompting.
- **Model Improvements**: Finetune vision-text models like Gemini-Vision for better medical procedure understanding.
- **Smart Glass Integration**: Extend compatibility to devices like Ray-Ban Meta glasses for seamless observation.
- **Global Deployment**: Deploy StitchWitch worldwide to revolutionize surgical procedures, reduce errors, and improve patient outcomes.

---

## **Built With**
- **asyncio**
- **gemini**
- **opencv**
- **python**
- **reflex**

---

import asyncio
import cv2
from concurrent.futures import ThreadPoolExecutor
import google.generativeai as genai
import json
import PIL.Image
import os
from functools import partial
import re
import glob
from pypdf import PdfReader


# Global agents
img_model = genai.GenerativeModel('gemini-pro-vision')
txt_model = genai.GenerativeModel('gemini-pro')

chat_model = genai.GenerativeModel('gemini-pro')
chat_agent = chat_model.start_chat()    

alert_model = genai.GenerativeModel('gemini-pro')
alert_agent = alert_model.start_chat()

chat_history = ''

# Bypassing security
safe = [
        {
            "category": "HARM_CATEGORY_DANGEROUS",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE",
        },
    ]
    
def remove_ctrl(txt):
  to_rem = re.findall('<ctr'+"(.*)"+'>', txt)
  if len(to_rem)>0:
    to_rem = '<ctr'+to_rem[0]+'>'
    txt = txt.replace(to_rem,'')
  
  return txt

async def gemini_call_async(frames_path, diagrams_lst, diagram_desc, procedure_doc, project_name, itr, executor):
    print(f"## Analyzing frames: {frames_path}")
    diag_prompt = "The following images contain labelled diagrams of human anatomy. Remember each part of the provided anatomy."
    desc_prompt = f" \n And following is the description of each part labelled in the images: \n\n {diagram_desc} \n ----- \n"

    # task_prompt = f"The surgeon is performing {surgery_name} in the following frames. Based on the above context, which exact part of the labelled anatomy is being operated on? Only return the name"
    task_prompt = f"The surgeon is performing {project_name.replace('_',' ')} in the following frames. Based on the above context, only describe what's exactly is in the images very briefly? Don't return general information"

    # read images from img path
    video_imgs = []
    for f in frames_path:
        video_imgs.append(PIL.Image.open(f[1]))

    # Asynchronously handle model invocation
    def image_agent_generate(diag_prompt, diagrams_lst, desc_prompt, task_prompt, video_imgs):
        response = img_model.generate_content([diag_prompt] + diagrams_lst + [desc_prompt] + [task_prompt] + video_imgs, safety_settings=safe)
        return response.text
    
    def chat_agent_call(chat_agent_system_prompt):
        chat_agent_system_prompt = remove_ctrl(chat_agent_system_prompt)
        response = chat_agent.send_message(content=[chat_agent_system_prompt], safety_settings=safe)
        return response.text

    def alert_agent_call(alert_prompt):
        alert_prompt = remove_ctrl(alert_prompt) # Sometimes these words cause Gemini to crash
        alert_response = alert_agent.send_message(content=[alert_prompt], safety_settings=safe)
        return alert_response.text

    
    response = await asyncio.get_event_loop().run_in_executor(executor, lambda: image_agent_generate(diag_prompt, diagrams_lst, desc_prompt, task_prompt, video_imgs))
    
    # Chat History Module:
    # Pass to chat agent to maintain history
    print(f"## {itr} ##")
    if itr==0:
        chat_agent_system_prompt = f"You are a surgery expert observing a {project_name}. Only note what surgeon is seen doing briefly. Avoid repeating and only output the new information. If nothing new, return empty string. \n\n **Procedure**: \n {response}"
    else:
        chat_agent_system_prompt = f"\n {response} \n Only note what surgeon is seen doing briefly. Avoid repeating and only output the new information. If nothing new, return empty string. \n"
    
    try:
        chat_response = await asyncio.get_event_loop().run_in_executor(executor, lambda: chat_agent_call(chat_agent_system_prompt))
        print(chat_response)

        # Modifying global variable to keep track of history
        global chat_history
        chat_history += chat_response
    except Exception as e:
        print(e)
        return 'ERROR'
    
    # Alerting Module
    a = "Return response in json format with structure {'warning': 'What should the surgeon be caution about at this stage', 'danger': 'Is the surgeon doing something risky? Be moderately critical! Answer true or false', 'danger_detail': 'Briefly describe what risk the surgeon is taking and how to reduce risk '}"
    if itr==0:
        alert_prompt = f"You are an expert surgeon. You will compare the standard procedure for {project_name} with observation and {a} \n\n **Standard Procedure**: \n {procedure_doc} \n\n **Observation**: {chat_response} \n"
    else:
        alert_prompt = f"\n {chat_response} \n {a} \n" 

    print("## ALERT MODULE ##")
    try:
        alert_response = await asyncio.get_event_loop().run_in_executor(executor, lambda: alert_agent_call(alert_prompt))
        print(alert_response)
    except Exception as e:
        print(e)
        return 'ERROR'
  
    # Creating a json response to return
    # Parse json to send to frontend
    resp = {}
    try:
        temp = re.findall('{(?:[^{}])*}',alert_response)[0]
        temp = temp.replace('False','false')
        temp = temp.replace('True','false')
        temp = temp.replace('json','')
        resp = json.loads(temp)
        resp['caption'] = chat_response
        resp['status'] = '200'

    except Exception as e:
        resp['status'] = '500'
        # print(resp)
        print(e)

    return resp


def get_instructional_material(project_name,file_loc):
    print(f"## Reading Instructional Material: {project_name}")
    # Read all imgs in project folder
    print(f"./data/img/{project_name}/*")
    files = glob.glob(f"./data/img/{project_name}/*") 
    print(files)
    diagrams_lst = []
    for d in files:
        diagrams_lst.append(PIL.Image.open(d))
    
    prompt = "The following images contains a labelled diagram of human anatomy. What labels you see and describe each briefly"
    labels = img_model.generate_content([prompt] + diagrams_lst , safety_settings=safe)
    
    # Reading standard procedure doc
    pdf_file = PdfReader(file_loc)

    # Find procedure for surgery_name
    all_txt = ''
    
    for page_no in range(len(pdf_file.pages)):
        print(f"Getting page {page_no}")
        all_txt += pdf_file.pages[page_no].extract_text()

    prompt = f"Find material in the following text relevant to '{project_name.replace('_',' ')}' and return a numbered list of detailed steps: \n\n {all_txt}"
    surgery_procedure = txt_model.generate_content(prompt,safety_settings=safe)
    
    return (diagrams_lst, labels.text, surgery_procedure.text)

    
async def capture_frames_from_video_async(video_path, output_folder, KPS, project_name, executor,file_loc):
    
    # Reading docs
    diagrams_lst, diagram_desc, procedure_doc = get_instructional_material(project_name,file_loc)
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Unable to open video file '{video_path}'")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    hop = round(fps / KPS)

    curr_frame = 0
    img_i = 0
    files_to_upload = []
    interval_len = 6
    interval_count = 0
    gemini_called = False
    initial_call = True

    while(True):
        if initial_call:
            # sleep(10)
            initial_call = False
        if gemini_called:
            for i in range(240):
                ret, frame = cap.read()
                gemini_called = False
        else:
            ret, frame = cap.read()
                
        if not ret:
            break
        if curr_frame % hop == 0:
            name = output_folder+'/frame' + str(img_i) + '.jpg'
            files_to_upload.append((img_i, name))
            img_i += 1
            print ('Creating...' + name)
            cv2.imwrite(name, frame)

            interval_count += 1
            # When interval_len frames have accumulated, call gemini
            if interval_count%interval_len==0:
                response = await asyncio.create_task(gemini_call_async(files_to_upload[-interval_len:], diagrams_lst, diagram_desc, procedure_doc, project_name, interval_count, executor))
                gemini_called = True
                yield response
        curr_frame += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()    

async def analyze_video_async(project_name,file_loc):
    json_file_path = 'env.json'
    video_path = f"data/video/{project_name}.mp4"
    print(f"{project_name}")

    with open(json_file_path, 'r') as file:
        config = json.load(file)
        google_api_key = config['GOOGLE_API_KEY']

    genai.configure(api_key=google_api_key)
    output_folder = "captured_frames"
    KPS = 1 # keyframes per second

    os.makedirs(output_folder, exist_ok=True)

    executor = ThreadPoolExecutor(max_workers=4)
    try:
        async for response in capture_frames_from_video_async(video_path, output_folder, KPS, project_name, executor, file_loc): 
            # print(response)
            yield (response,True)
    finally:
        executor.shutdown()


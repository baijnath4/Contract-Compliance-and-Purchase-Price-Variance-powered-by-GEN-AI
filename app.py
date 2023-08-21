from flask import Flask, render_template, request, url_for, redirect, session,jsonify
import os
from pdfminer.high_level import extract_text
import openai
import pandas as pd
import sys



from utils.api_utils import documentChatBot, genericChatbot
from chatGPTModel.gPTModel import contractandinvoice, contractandpo,threewaymatch,questions

# sys.path.insert(0, 'C:/Users/01934L744/Box/Baijnath Data/Project 2023/Nidhi/contract - v4.1/chatGPTModel')

po_data = pd.DataFrame()
app = Flask(__name__)
app.secret_key = 'hello'

UPLOAD_FOLDER_pdf = "upload/"

UPLOAD_FOLDER_3way = "upload_3way/"
DUMMY = "dummy/"


def dataFromPayload(request):
    payload = request.get_json()
    input_data = payload['text']
    return input_data

def fun_file():
    fCount = 0
    dictfile = {}
    for file in os.listdir('upload/'):
        
        path = os.path.join(UPLOAD_FOLDER_pdf,file)
        doc_text_ppv = extract_text(path)
        dictfile[fCount] = [file,doc_text_ppv]
        fCount=fCount+1
    return dictfile,fCount

def fun_file_dummy():    
    dictfileDumm = {}
    for file in os.listdir('dummy/'):
        path = os.path.join(DUMMY,file)
        dummPD = pd.read_excel(path)
        dictfileDumm[file] = dummPD      
    return dictfileDumm

current_file_index = 0
promptDropDown = {}



fileContent1_3way = pd.DataFrame()
dummy_data = pd.DataFrame()

@app.route('/')
def index():
    dummy_data = pd.DataFrame()
    fileContent1_3way = pd.DataFrame()

    return render_template('./3waymatch v5.html', dummy_data = dummy_data,fileContent1_3way = fileContent1_3way)



@app.route('/uploadfile', methods = ['GET','POST'])
def uploadfile():                     #  Comparative analysis  - file upload
    upload = True
    fileCount = 0
    dummy_data = pd.DataFrame()
    fileContent1_3way = pd.DataFrame()
    if request.method == 'POST':
        try:
            f = request.files.getlist('doc_in_upload')
        except:
            f = request.files.getlist('doc_in_upload_3way')
        for fa in f:  
            path = os.path.join(UPLOAD_FOLDER_pdf,fa.filename)
            
            fa.save(path)
        fileContDict,fileUplCount= fun_file()
        current_file = fileContDict[current_file_index][0]
 
        return render_template('./3waymatch v5.html',fileContent1_3way=fileContent1_3way,dummy_data=dummy_data, current_file = current_file, fileContent1 = fileContDict[current_file_index][1] ,fileCount=fileUplCount)
        
    return render_template('./3waymatch v5.html')



@app.route('/next')
def next():
    global current_file_index
    current_file_index = current_file_index + 1
    fileContent1_3way = pd.DataFrame()
    fileContDictnext,fileUplCount= fun_file()
    
    if current_file_index >= len(fileContDictnext):
        current_file_index = 0

    current_file = fileContDictnext[current_file_index][0]
    dumm_dic = fun_file_dummy()
    
    dummFileName = current_file.split('.')[0]+'.xlsx'
    dummy_data = dumm_dic[dummFileName]
    
 

    return render_template('./3waymatch v5.html',dummy_data=dummy_data,fileContent1_3way=fileContent1_3way,current_file= current_file, fileContent1 = fileContDictnext[current_file_index][1] ,fileCount=fileUplCount)

@app.route('/previous')
def previous():
    global current_file_index
    fileContent1_3way = pd.DataFrame()
    po_data = pd.DataFrame()
    fileContDictPrevious,fileUplCount= fun_file()
    if current_file_index <= 0:
        current_file_index = fileUplCount-1
        
        fileContent1 = fileContDictPrevious[current_file_index][1]        
    else:
        current_file_index = current_file_index - 1
        fileContent1 = fileContDictPrevious[current_file_index][1]
    current_file = fileContDictPrevious[current_file_index][0]

    dumm_dic = fun_file_dummy()    
    dummFileName = current_file.split('.')[0]+'.xlsx'
    dummy_data = dumm_dic[dummFileName]
    return render_template('./3waymatch v5.html',dummy_data=dummy_data,fileContent1_3way = fileContent1_3way,current_file = current_file, fileContent1 = fileContent1 ,fileCount=fileUplCount)

@app.route('/get_result_docInsight', methods=['POST'])    # drop down 
def get_result_docInsight():
    selected_option = request.form['selected_option']
    fileContDict,fileUplCount= fun_file()
    fileContent1 = fileContDict[current_file_index][1]
    questionResult = questions(fileContent1,selected_option)
    # Perform any necessary processing with the selected option
    result = f"{questionResult}"
    promptDropDown[selected_option] = result
    # jeson_result = jsonify(promptDropDown=promptDropDown)
    print("promptDropDown:---",promptDropDown)
    return  promptDropDown



#  chat boat ....................................................................

@app.route("/document_chatbot", methods=['POST'])
def qaChatBot():
    payload = request.get_json()
    fileContDict,fileUplCount= fun_file()
    fileContent1 = fileContDict[current_file_index][1]

    return documentChatBot(fileContent1, payload['question'])

@app.route("/global_chatbot", methods=['POST'])
def globalChatBot():
    payload = request.get_json()   
    return genericChatbot(payload['question'])

# 3Way Match  ..............................................................

def fun_file_3way():
    fCount = 0
    dictfile = {}
    for file in os.listdir('upload_3way/'):
     
        path = os.path.join(UPLOAD_FOLDER_3way,file)
        doc_text_ppv = pd.read_excel(path)
        dictfile[fCount] = [file,doc_text_ppv]
        fCount=fCount+1

    return dictfile,fCount

def analysisResult():
    
    filePdfDic,fileUplCount= fun_file()
    current_file = filePdfDic[current_file_index][0]
    dumm_dic = fun_file_dummy()
    dummFileName = current_file.split('.')[0]+'.xlsx'
    dummy_data = dumm_dic[dummFileName]
    # contractDummy = pd.read_excel("C:/Users/01934L744/Box/Baijnath Data/Project 2023/Nidhi/contract - v4.1/dummy/C0_1L976.xlsx")
    po = pd.read_excel("upload_3way/PO.xlsx")
    invoice = pd.read_excel("upload_3way/Invoice data.xlsx")

    # po = pd.read_excel("C:/Users/01934L744/Box/Baijnath Data/Project 2023/Nidhi/contract - v4.1/upload_3way/PO.xlsx")
    # invoice = pd.read_excel("C:/Users/01934L744/Box/Baijnath Data/Project 2023/Nidhi/contract - v4.1/upload_3way/Invoice data.xlsx")
    resContPO, sumContPo = contractandpo(contract=dummy_data,po=po)
    resContInvoice, sumContInvoice = contractandinvoice(contract=dummy_data, invoice=invoice)
    res3WayMatch, sum3WayMatch = threewaymatch(contract=dummy_data, po=po,invoice=invoice)  
    return resContPO,sumContPo,resContInvoice,sumContInvoice,res3WayMatch,sum3WayMatch
    

@app.route('/uploadfile_3way', methods = ['GET','POST'])
def uploadfile_3way():                     #  Comparative analysis  - file upload

    fileUplCount_3way = 0
    if request.method == 'POST':
        f = request.files.getlist('doc_in_upload_3way')
        for fa in f:  
            path = os.path.join(UPLOAD_FOLDER_3way,fa.filename)
            fa.save(path)
        fileContDict_3way,fileUplCount_3way = fun_file_3way() 
        current_file_3way = fileContDict_3way[current_file_index][0].split('.')[0]
        resContPO,sumContPo,resContInvoice,sumContInvoice,res3WayMatch,sum3WayMatch=analysisResult()
        return render_template('./3waymatch v5.html', resContPO=resContPO,sumContPo=sumContPo,resContInvoice=resContInvoice,sumContInvoice=sumContInvoice,res3WayMatch=res3WayMatch ,sum3WayMatch=sum3WayMatch, current_file_3way = current_file_3way, fileContent1_3way = fileContDict_3way[current_file_index][1] ,fileUplCount_3way = fileUplCount_3way, dummy_data=dummy_data)        
    return render_template('./3waymatch v5.html')

current_file_index_3way_upload = 0
@app.route('/next_3way')
def next_3way():
    global current_file_index_3way_upload
    # current_file_index_3way_upload = current_file_index_3way_upload + 1

    dummy_data = pd.DataFrame()
    fileContDictnext_3way,fileUplCount= fun_file_3way()
    if current_file_index_3way_upload >= len(fileContDictnext_3way):
        # current_file_index_3way_upload = 0
        current_file_index_3way_upload = current_file_index_3way_upload + 1
    fileContent1_3way = fileContDictnext_3way[current_file_index_3way_upload][1]
    print("3Way fileContent1_3way",fileContent1_3way)
    
    current_file_3way = fileContDictnext_3way[current_file_index_3way_upload][0]
    resContPO,sumContPo,resContInvoice,sumContInvoice,res3WayMatch,sum3WayMatch=analysisResult()
    return render_template('./3waymatch v5.html',resContPO=resContPO,sumContPo=sumContPo,resContInvoice=resContInvoice,sumContInvoice=sumContInvoice,res3WayMatch=res3WayMatch ,sum3WayMatch=sum3WayMatch,dummy_data=dummy_data,current_file_3way= current_file_3way, fileContent1_3way = fileContent1_3way ,fileCount=fileUplCount)

@app.route('/previous_3way')
def previous_3way():
    global current_file_index
    dummy_data = pd.DataFrame()
    fileContDictPrevious_3way,fileUplCount= fun_file_3way()
    
    if current_file_index <= 0:
        current_file_index = fileUplCount-1
        
        fileContent1_3way = fileContDictPrevious_3way[current_file_index][1]        
    else:
        current_file_index = current_file_index - 1
        fileContent1_3way = fileContDictPrevious_3way[current_file_index][1]
    current_file_3way = fileContDictPrevious_3way[current_file_index][0]
    resContPO,sumContPo,resContInvoice,sumContInvoice,res3WayMatch,sum3WayMatch=analysisResult()
    return render_template('./3waymatch v5.html',resContPO=resContPO,sumContPo=sumContPo,resContInvoice=resContInvoice,sumContInvoice=sumContInvoice,res3WayMatch=res3WayMatch ,sum3WayMatch=sum3WayMatch,dummy_data=dummy_data,current_file_3way = current_file_3way, fileContent1_3way = fileContent1_3way ,fileCount=fileUplCount)


if __name__ == '__main__':
    app.run(debug=True)

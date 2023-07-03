import os
import sys
import requests
import json
from pdf2image import convert_from_bytes,convert_from_path
from PIL import Image
import time
class requestAzure:
    def __init__(self, Filename):
        # Azure Computer vision details taken from Azure portal, need replacing when used

        subscription_key = ""                                       #this needs to be taken from your own azure Form recognizer instance
        endpoint=""                                                 #this too comes from your azure form recognizer
        # ocr_url = endpoint + "vision/v2.0/ocr"
        ocr_url = endpoint + "formrecognizer/v2.1-preview.3/layout/analyze"
        headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type':"application/pdf"}
        # params = {'language': 'unk', 'detectOrientation': 'true'}
        params = {}
        self.analysisfile = "json/Layout-Result-" + '.'.join(Filename.split('/')[-1].split('.')[:-1]) + ".pdf.json"

        if Filename[-3:]=="pdf":

            #Finding the file to use
            #Convert from .pdf to .jpg and save as .jpg

            # DataConvert=convert_from_path(Filename,poppler_path=(r"C:\Program Files\poppler-0.68.0_x86\bin"))
            # DataConvert=convert_from_path(Filename)
            # JpgPath=Filename[0:-4]+".jpg"
            #
            # First_page=DataConvert[0]
            # First_page.save(JpgPath, "JPEG")

            #Open jpg and apply params/headers for Azure Cloud Vision
            print(Filename)
            DataJpg=open(Filename,"rb").read()

            response = requests.post(ocr_url, params=params, headers=headers,data=DataJpg)
            url = response.headers["Operation-Location"]
            print(response.text)

            # print(response.raise_for_status())
            #json output from Azure
            # response = response.decode('utf-8')
            #analysis = response.json()
            time.sleep(5)
            analysis = requests.get(url,headers = {'Ocp-Apim-Subscription-Key': subscription_key}).json()
            while analysis["status"] == "running" :
                time.sleep(1)
                analysis = requests.get(url,headers = {'Ocp-Apim-Subscription-Key': subscription_key}).json()


        elif Filename.split('.')[-1][:2] == "jp":

            #open jpg and Azure Cloud vision Params/Headers
            DataJpg=open(Filename,"rb").read()

            response = requests.post(ocr_url , params=params, headers=headers,data=DataJpg)
            url = response.headers["Operation-Location"]
            response.raise_for_status()

            #json output from Azure
            time.sleep(5)
            analysis = requests.get(url,headers = {'Ocp-Apim-Subscription-Key': subscription_key}).json()
            while analysis["status"] == "running" :
                time.sleep(1)
                analysis = requests.get(url,headers = {'Ocp-Apim-Subscription-Key': subscription_key}).json()


        elif Filename[-3:]=="png":

            #Convert from png to jpg, save load etc
            NewFile=Image.open(Filename)
            JpgPath=Filename[0:-4]+".jpg"

            NewFile.save(JpgPath)
            #open jpg and Azure Cloud vision Params/Headers
            DataJpg=open(JpgPath,"rb").read()

            response = requests.post(ocr_url, params=params, headers=headers, data=DataJpg)
            url = response.headers["Operation-Location"]
            response.raise_for_status()

            #json output from Azure
            time.sleep(5)
            analysis = requests.get(url,headers = {'Ocp-Apim-Subscription-Key': subscription_key}).json()
            while analysis["status"] == "running" :
                time.sleep(1)
                analysis = requests.get(url,headers = {'Ocp-Apim-Subscription-Key': subscription_key}).json()


        else:
            Exception("Invalid file format")

        with open(self.analysisfile, "w") as f:
            json.dump(analysis, f, indent = 4)

        print(f"Received analysis successfully: {self.analysisfile}")




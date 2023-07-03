# Training Certificate Cataloguing Tools

<img width="1000" alt="Training Certificate Cataloguing Tool Thumbnail" src="https://github.com/Projecting-Success-Solutions-Portal/Project-Data-Analytics-Solutions/assets/30728931/8499560f-63d3-43d8-90f8-12cabeaaa232">

<br />

**Solution Description**

**User story** – This solution is a tool that can autonomously catalogue and parse a set of training certificates (as PDF files) to record its data. This tool can record data such as the training body, course name, country or city, certification date, employee name or any other information from the certificate that may be relevant. It is able to do this regardless of the language, layout, or file type of the certificate.

**Persona** – This tool is for a HR manager/ administrator, allowing them to automatically extract information from training certificates.

**Data** – The data consists of some example templates/ certificates; however, it doesn’t require any data apart from the certificate files to be scanned.



**Solution Detailed Description**

The solution consists of a collection of python scripts, and some folders which store templates/ json data. The scripts are:
Main.py, which is the script which is run in the terminal.
PDFparser.py, which sends the PDF to Microsoft azure form recognizer, and produces a json file
JSONparser.py which extracts the information needed from the json file, either by using a template from the folder, or by calling a GUI for the user to draw a new template.
GUIbits.py handles the running of the GUI


**Solution Review**

Insights – This is a useful tool that would save a lot of time when processing lots of certificates of the same type. Could be improved by making a full UI, not just for the template drawing part. Set up is quite involved for someone without python experience.

<img width="1000" alt="Maturity Matrix" src="https://github.com/Projecting-Success-Solutions-Portal/Project-Data-Analytics-Solutions/assets/30728931/7dc96a63-7b5b-4199-98bd-6812a1e8e55f">

<br /><br />

**To watch the Demonstration of the application please click the image below:**
<br /><br />
<div align="center">
      <a href="https://www.youtube.com/watch?v=GwEimEYRNG0">
     <img 
      src="https://github-production-user-asset-6210df.s3.amazonaws.com/30728931/250547491-09137834-fa41-4a18-8f91-0b2635ea12fc.png" 
      alt="Training Certificate Cataloguing Tools" 
      style="width:100%;">
      </a>
    </div>

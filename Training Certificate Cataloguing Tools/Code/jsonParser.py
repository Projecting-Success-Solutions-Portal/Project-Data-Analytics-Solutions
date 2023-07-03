import numpy as np
import pandas as pd
from pprint import pprint
import os
import json
import argparse
from glob import glob
from guiBits import TemplateCreator


"""
Utilise information parsed by Azure and output data for requested fields
"""
class JSONcertificate:
    def __init__(self,filename, **info):
        self._filename = filename
        with open(filename, 'r', encoding='utf-8-sig') as f:
            self._jsondata = json.load(f)
        self._result = []
        print('info', info)
        self._template = info.get('templatefile', None)
        self._originalfile = info.get('originalfile', None)


    """
    Print out parsed information from json file
    """
    def show(self):
        for line in self._jsondata['analyzeResult']['readResults'][0]['lines']:
            print("{} - {}".format(line['boundingBox'], line['text']))


    """
    Get box in the full format with 8 coordinates
    """
    @staticmethod
    def standardBox(m):
        if (len(m) == 8):
            pass
        elif (len(m) == 4):
            # expecting left top corner x,y; right bottom corner x,y
            return [m[0],m[1],m[2],m[1],m[2],m[3],m[0],m[3]]
        else:
            Exception("Expected mask in the form of 4 coordinates dictionary")


    """
    Give a measure of distance between boxes: sums up all outstanding paddings
    """
    @staticmethod
    def distance(mask, box):
        dx = 0; dy = 0;

        dx += np.maximum( (mask[0] - box[0]), 0)
        dx += np.maximum(-(mask[2] - box[2]), 0)
        dx += np.maximum(-(mask[4] - box[4]), 0)
        dx += np.maximum( (mask[6] - box[6]), 0)

        dy += np.maximum( (mask[1] - box[1]), 0)
        dy += np.maximum( (mask[3] - box[3]), 0)
        dy += np.maximum(-(mask[5] - box[5]), 0)
        dy += np.maximum(-(mask[7] - box[7]), 0)

        diff = np.abs(dx) + np.abs(dy)

        return diff


    """
    Set used template by name directly
    """
    def set_template(self,name):
        self._template = name


    """
    Identify template from a set of keywords if not fixed otherwise
    """
    def pick_template(self):
        if (self._template): return self._template

        fulltext = ""
        for line in self._jsondata['analyzeResult']['readResults'][0]['lines']:
            fulltext += " " + line['text'].lower()

        # print(fulltext)

        matches = []
        for tname in glob('templates/*.json'):
            with open(tname, 'r', encoding='utf-8-sig') as file:
                tmp = json.load(file)
                keywords = tmp.get('keywords', [])
                if (type(keywords) != list):
                    keywords = [keywords]
                match = True

                for key in keywords:
                    if not(key.lower() in fulltext):
                        match = False
                        break

                if (match):
                    matches.append(tname)

        if not(len(matches)):
            Exception("Found no matching template.")
        elif (len(matches) == 1):
            return matches.pop()
        else:
            matches = sorted(matches)
            ###################################################
            #  TODO: Prompt user to select a template  in GUI #
            ###################################################
            print('Found several matching templates:')
            for i in range(len(matches)):
                print(f'{i+1} : {matches[i]}')
            while (True):
                i = int(input('Choose template: ')) - 1
                if (i < len(matches)):
                    return matches[i]


    """
    Figure out the template, retrieve data from loaded JSON file with template mask and save result
    """
    def parse(self):
        templatefile = self.pick_template()
        result = []
        resdict = {}

        # Parse masked fields
        if not(templatefile):
            print(templatefile)
            if (self._originalfile):
                tc = TemplateCreator(self._originalfile)
                templatefile = tc.templatefile
            else:
                Exception("Original file unknown.")

            print('templatefile', templatefile)
            # self.parse_generic()
            # return
        #     pass
        # else:

        with open(templatefile, 'r', encoding='utf-8-sig') as file:
            template = json.load(file)

        lines = self._jsondata['analyzeResult']['readResults'][0]['lines']
        resdict = {'template': templatefile.split('/')[-1][:-5]}
        if ("LMS ID" in template):
            resdict["LMS ID"] = template["LMS ID"]
        maxpadding = 0.05
        confidence = 1

        # Check all masked fields
        if (template.get('fields', None)):
            for field, box in template['fields'].items():
                if not(len(box)):
                    continue
                collect = []
                for i in range(len(lines)):
                    line = lines[i]
                    words = line['words']
                    for word in words:
                        distance = self.distance(self.standardBox(box), word['boundingBox'])
                        if (distance < maxpadding):
                            collect.append(word['text'])
                            confidence = np.minimum(confidence, word['confidence'])

                resdict[field.lower()] = ' '.join(collect)

        resdict['confidence'] = confidence

        # look out for tables
        tables = self._jsondata['analyzeResult']['pageResults'][0]['tables']
        if not(len(tables)):
            result = [resdict]
        else:
            tableDict = template.get('Table', {})

            tabulardict = {}
            for table in tables[:1]:
                colname = {}
                rowidx = 0
                line = {}
                for cell in table['cells']:
                    if cell['isHeader']:
                        colname[cell['columnIndex']] = tableDict.get(cell['text'], cell['text'])
                        rowidx = cell['rowIndex']
                    else:
                        if (cell['rowIndex'] != rowidx):
                            rowidx = cell['rowIndex']
                            if (line.keys()):
                                sumdict = resdict.copy()
                                sumdict.update(line)
                                sumdict = {k.lower(): v for k, v in sumdict.items()}
                                result.append(sumdict)
                            line = {}

                        key = colname[cell['columnIndex']]
                        line[key] = cell['text']

                if (line.keys()):
                    sumdict = resdict.copy()
                    sumdict.update(line)
                    result.append(sumdict)

        self._result = result


    """
    General parsing if working with photos or template failed
    """
    def parse_generic(self):
        for line in self._jsondata['analyzeResult']['readResults'][0]['lines']:
            print(line['text'])
        pass


    """
    Output result according to the format specified
    """
    def output(self, file=None):
        columns = [
                    'name',
                    'issue info',
                    'company',
                    'certificate type',
                    'course title',
                    'LMS ID',
                    'training period',
                    'training provider',
                    'valid until',
                    'template',
                    'confidence',
                  ]
        df = pd.DataFrame([], columns = columns)

        # print(len(self._result))
        # for i in range(len(self._result)):
        #     print(self._result[i])

        for res in self._result:
            df = df.append(res, ignore_index=True)[columns]

        # look up ids
        # ids = df[' ID']
        # self.get_LMSIDs(self._result
        # print('tabular: ', self._result.get('tabular', []))

        df = df.fillna('')

        print(df)
        if (file):
            df.to_csv(file, mode='a', header=not(os.path.exists(file)))


# def main(**kwargs):
#     # a = JSONcertificate(kwargs.get('file', 'json/Layout-Result-Funiecatene.pdf.json'))
#     a = JSONcertificate(kwargs.get('file', 'json/Layout-Result-Cypress1.pdf.json'))
#     # a.show()
#     a.parse()
#     a.output('output/test.csv')
#
#
# if (__name__ == '__main__'):
#
#     parser = argparse.ArgumentParser()
#     parser.add_argument('-f',  '--file',  type=str,  dest='file')
#     args = parser.parse_args()
#
#     kwargs = {}
#     if (args.file != None): kwargs['file'] = args.file
#
#     main(**kwargs)
#




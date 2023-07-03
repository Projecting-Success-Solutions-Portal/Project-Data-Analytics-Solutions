from jsonParser import JSONcertificate
from pdfParser import requestAzure
# from get_coordinates import DrawRectangle
import argparse
import sys
import os


def main(**kwargs):

    for f in kwargs.get('files'):
        info = {}
        if (f.split('.')[-1] != 'json'):
            ###########################################################
            #  TODO: fix automatic fetch of the JSON file from Azure  #
            ###########################################################
            A = requestAzure(f)
            analysisfile = A.analysisfile
            pdfname = f.split('/')[-1]
            analysisfile = 'c:/Users/44771/Documents/Code/json/Layout-Result-' + pdfname + '.json'  #change to the correct file path 
            info['originalfile'] = f
            # pass
        else:
            analysisfile = f
        # print(f)
        print(info)

        # info['originalfile'] = "Certificates/1-Single/Cypress1.pdf"
        info['templatefile'] = kwargs.get('templatefile', None)
        a = JSONcertificate(analysisfile, **info)
        a.parse()
        a.output(kwargs.get('output', 'out.csv'))


if (__name__ == '__main__'):

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', nargs='+', dest='files', help='Supply a list of files')
    parser.add_argument('-o',  type=str,  dest='output', help='Specify output file (csv)')
    parser.add_argument('-t',  type=str,  dest='templatefile', help='Specify template file')

    args = parser.parse_args()
    if len(sys.argv) < 2:
        parser.print_usage()
        sys.exit(1)

    kwargs = {}
    if (args.files != None): kwargs['files'] = args.files
    if (args.output != None): kwargs['output'] = args.file
    if (args.templatefile != None): kwargs['templatefile'] = args.templatefile

    main(**kwargs)



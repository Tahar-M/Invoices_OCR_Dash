import pytesseract
from pytesseract import Output
import cv2
import re
import json

class Extract_data_OCR:

    def __init__(self,img_path):
        
        self.img_path = img_path

        self.img = cv2.imread(self.img_path)
      
        self.d = pytesseract.image_to_data(self.img, output_type=Output.DICT)

        self.d['text'] = [s.lower() for s in self.d['text']]

        self.n_boxes = len(self.d['text'])


        self.list_index = [ i for i in range(self.n_boxes) if self.d['text'][i] != '']

        self.done_index = []

        self.lines_by_coordinates = {}

        self.g_centre = []

        self.lines = []

        self.ID = None

        self.p = '[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+'

        with open('layout.json','r') as  j:
            self.layout = json.load(j)

        self.whole_string = None

        self.data_dic = {}


    def extract_amount_fac(self,string):

        

        return float(re.findall(self.p,string)[0].replace(',',''))


    def extract_n_tva(self,string):

    

        s = string[string.find('numero tva'):string.find('numero tva')+18]

        return re.findall(self.p,s)[0].replace(',','')



    def get_lines(self):

        for k in self.list_index:

            if k not in self.done_index:

                L = [k]

                self.done_index.append(k)

                for j in self.list_index:

                    if j not in self.done_index:

                        if abs((self.d["top"][k]+ (self.d['height'][k]/2)) - ((self.d["top"][j]+ (self.d['height'][j]/2))))<=self.d['height'][k]/4:

                            L.append(j)
                            self.done_index.append(j)
                self.lines.append(L)
                self.g_centre.append(self.d["top"][k]+ (self.d['height'][k]/2))

    def extract_data(self):

        



        self.data_dic = {self.g_centre[i]: ' '.join([self.d['text'][i] for i in line]) for i,line in enumerate(self.lines) }

        self.whole_string = ' '.join(self.data_dic.values())
        

        self.ID = self.extract_n_tva(self.whole_string)

        self.data_dic = {u:self.data_dic[v] for u,v in self.layout[self.ID].items()}



    def get_data(self):

        self.get_lines()
        self.extract_data()


        if self.ID=='1230':

            r = {'date': '/'.join(re.findall(self.p,self.data_dic['date'])),
            'N_tva': re.findall(self.p,self.data_dic['N_tva'])[0],
            'N_facture': (re.findall(self.p,self.data_dic['N_facture'].replace('/',''))[0]),
            'HT': round(self.extract_amount_fac(self.data_dic['HT']),2),
            'Taxe': round(self.extract_amount_fac(self.data_dic['HT'])*0.2,2),
            'TVA': '20.00%',
            'TTC': round(self.extract_amount_fac(self.data_dic['TTC'].replace('/','7')),2)}

            return r

        elif self.ID=='1231':
            r = {'date': '/'.join(re.findall(self.p,self.data_dic['date'])),
            'N_tva': re.findall(self.p,self.data_dic['N_tva'])[0],
            'N_facture': re.findall(self.p,self.data_dic['N_facture'])[0],
            'HT': round(self.extract_amount_fac(self.data_dic['HT']),2),
            'Taxe': round(self.extract_amount_fac(self.data_dic['HT'])*0.2,2),
            'TVA': '20.00%',
            'TTC': round(self.extract_amount_fac(self.data_dic['TTC']),2)}

            return r

        elif self.ID == '1232':
            r = {'date': '/'.join(re.findall(self.p,self.data_dic['date'])[1:]),
            'N_tva': re.findall(self.p,self.data_dic['N_tva'])[0],
            'N_facture': (re.findall(self.p,self.data_dic['N_facture'].replace('/',''))[0]),
            'HT': round(self.extract_amount_fac(self.data_dic['HT']),2),
            'Taxe': round(self.extract_amount_fac(self.data_dic['HT'])*0.2,2),
            'TVA': '20.00%',
            'TTC': round(self.extract_amount_fac(self.data_dic['TTC']),2)}

            return r 
        else:
            
            print('Facture inconnue')




    




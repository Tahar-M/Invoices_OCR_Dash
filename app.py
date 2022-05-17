import pandas as pd
import streamlit as st
from datetime import datetime
import plotly.express as px
import pdf2image

import extract_data_ocr


data = pd.read_csv('data.csv')
data['date'] = data['date'].apply( lambda date : datetime.strptime(date,"%d/%m/%Y") )
labels= {'1230':'Fournisseur 1', '1231': 'Fournisseur 2','1232': 'Fournisseur 3'}

data['fournisseur']= data['N_tva'].apply( lambda x : labels[str(x)])

data = data.sort_values(by=["date"],ascending=True )


data= data.set_index('date')

st.title('Suivi des dépenses fournisseurs')

cl1, cl2 = st.columns(2)

with cl1:
    start_date = st.date_input('Début',value = min(data.index), min_value= min(data.index),  max_value=max(data.index))
    

with cl2:
    end_date = st.date_input('Fin',value = max(data.index), min_value= start_date,  max_value=max(data.index))


st.success(f'Période  :  Du {start_date} au {end_date}')


data = data.loc[start_date:end_date]

data2 = data.copy()

data2 = data2.reset_index()







col1, col2, col3 = st.columns(3)

col1.metric("Nombre de fournisseurs", f"{len(set(data.N_tva))}")
col2.metric("Nombre de Factures", f"{len(set(data.N_facture))}")
col3.metric("Total ", f"{round(data.TTC.sum(),2)} €")


fig = px.pie(data, values='TTC', names='fournisseur', color='N_tva',hole=0.5)

fig.update_layout(
    title={
        'text': "Répartion des depenses par Fournisseurs ",
        'x':0.45,
        'xanchor': 'center',
        'yanchor': 'top'})

st.plotly_chart(fig, use_container_width=True)

data2 = data2.sort_values(by=["date"],ascending=True )

data2['year'] = [t.year for t in data2.date]
data2['month'] = [t.month for t in data2.date]
data2 = data2.groupby(['year','month','fournisseur']).TTC.apply(sum).reset_index()
data2["period"] = data2["year"].astype(str) +'-'+ data2["month"].astype(str)


fig2 = px.bar(data2, x='period', y="TTC",color='fournisseur',labels={
                     "TTC": "TTC en €",
                     "period": "Date par mois",
                     "fournisseur": "Fournisseur"
                 } )
fig2.layout.xaxis.tickvals = pd.date_range(str(start_date), str(end_date), freq='MS')
fig2.layout.xaxis.tickformat = '%b-%y'
fig2.update_layout(
    title={
        'text': "Dépenses par mois ",
        'x':0.45,
        'xanchor': 'center',
        'yanchor': 'top'})
st.plotly_chart(fig2, use_container_width=True)

fig3 = px.box(data,x='fournisseur', y="TTC", color='fournisseur',labels={
                     "TTC": "TTC en €",
                     "fournisseur": "Fournisseur",
                     "fournisseur": "Fournisseur"})

for s in data.fournisseur.unique():
    fig3.add_annotation(x=s,
                       y = data[data['fournisseur']==s]['TTC'].max(),
                       text = 'count factures = ' +str(len(data[data['fournisseur']==s]['TTC'])),
                       yshift = 10,
                       showarrow = False
                      )
fig3.update_layout(
    title={
        'text': "Stats par Fournisseur ",
        'x':0.45,
        'xanchor': 'center',
        'yanchor': 'top'})

st.plotly_chart(fig3, use_container_width=True)

with st.expander("Export des données"):

    st.dataframe(data)

    csv = data.to_csv().encode('utf-8')

    

    st.download_button(
        label="Export data as CSV",
        data=csv,
        file_name='data_sheet.csv',
        mime='text/csv',
         )

st.subheader('Traitement de facture par OCR:', anchor=None)

imagem_referencia = st.file_uploader("choisissez une facture sous forme pdf* : ", type=["pdf"],accept_multiple_files=False)

if imagem_referencia is not None:

    agree = st.checkbox('Prendre en compte dans la BDD')

button = st.button("Confirmer")


if button and imagem_referencia is not None:
    with st.spinner('Veuillez attendre SVP '):
    

        try:

            if imagem_referencia.type == "application/pdf":
                images = pdf2image.convert_from_bytes(imagem_referencia.read(),800)
                for page in images:
                    page.save('recent_upload.jpg', 'JPEG')

                a = extract_data_ocr.Extract_data_OCR('recent_upload.jpg')
                r = a.get_data()
                st.write('Extracted results')
                st.json(r)
                
                if agree:
                    df = pd.read_csv('data.csv')
                    r_dictionary = pd.DataFrame([r])
                    output = pd.concat([df, r_dictionary], ignore_index=True)
                    output.to_csv('data.csv',index=False)

                    st.success('Data extracted and saved properly')


                else:
                    st.success('Data extracted properly')


                


        except:
            st.error('Invoice Unkown, Please contact [Konta.tech](https://konta.tech/) for better service ')


with st.expander('About the app', expanded=False):

    st.markdown("""

Ce projet est un POC fortement inspiré de [Konta.tech](https://konta.tech/).

<h1>Use Case :</h1>

<h3>-Reporting des dépenses fournisseurs : </h3>
<ul>
     <p>En fonction de la période choisie, l'utilisateur à accès:<p>
<ul>
  <li>Le nombre des fournisseurs</li>
  <li>Le nombre de factures traitées</li>
  <li>Le total des dépenses fournisseurs</li>
  <li>La répartition des dépenses par fournisseurs</li>
  <li>La répartition des dépenses par mois</li>
  <li>Les statistiques des dépenses par fournisseur</li>
  <li>L'ensemble du Data Sheet de la période spécifiée sous forme csv
</ul>
</ul>
<h3>-Traitement de la facture et extraction des données par OCR  : </h3>
<ul>
<p> En téléchargeant une facture prise en charge par l'outil, l'utilisateur peut récupérer automatiquement :
<ul>
  <li>La date d'émission de la facture</li>
  <li>Le numéro de la facture</li>
  <li>Le numéro de TVA</li>
  <li>Le montant hors TVA</li>
  <li>Le taux de la taxe TVA</li>
  <li>Le montant de la taxe TVA</li>
  <li>Le montant TTC</li>
</ul>
<p>L'utilisateur à le choix d'inclure le résultat de l'extraction dans le reporting </p>
</ul>

""",unsafe_allow_html=True)
    st.write("Des exemples pour tester l'outil sont disponibles [ici](https://github.com/Tahar-M/Invoices_OCR_Dash/tree/main/exemples)")

    st.markdown("""
<h4>Comment ca marche ?</h4>

<p>Pour le moment, L'outil ne traite que 3 types de factures (3 fournisseurs) <strong>sous forme digitale.</strong></p>
<p> On utilise l'OCR open-source Tesseract pour récupérer les mots et leurs coordonnées.</p> 

<p>Pour chaque type de facture, on enregistre manuellement les coordonnées verticales des lignes contenantes les informations ciblées dans <em>layout.json </em> </p>

<p>   &nbsp;&nbsp;&nbsp;<strong>N.B:</strong> cette approche n'est compatible qu'avec les factures sous forme digitale (non scanné)</p>


<p>On construit après les lignes de la facture et leurs coordonnées.</p>
<p>En fonction de l'identifiant de la facture <em>'N_tva'</em>, on filtre les lignes en fonction du layout correspondant.</p>
On récupere après l'information en appliquant Regex. </p>

<br>
<p> Les données ont été générées aléatoirement en utilisant Python (openpyxl)</p>

<br>
<br>

<h5>Made by : <strong> Tahar Moumen </strong> </h5>
<p><strong> Email : </strong> tahar.moumen@outlook.com </p>
<p><strong> Tel : </strong> +212657497185 </p>

[![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/tahar-moumen/)
""",unsafe_allow_html=True)


    with open("CV_Tahar_en.pdf", "rb") as pdf_file:
        PDFbyte = pdf_file.read()

    st.download_button(label="CV Tahar Moumen",
                    data=PDFbyte,
                    file_name="CV_Tahar_en.pdf",
                    mime='application/octet-stream')
















    


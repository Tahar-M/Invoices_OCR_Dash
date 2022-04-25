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

cl1, cl2 = st.columns(2)

with cl1:
    start_date = st.date_input('From',value = min(data.index), min_value= min(data.index),  max_value=max(data.index))
    

with cl2:
    end_date = st.date_input('Until',value = max(data.index), min_value= start_date,  max_value=max(data.index))


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
        'text': "Repartion des depenses par Fournisseurs ",
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
        'text': "Depenses par mois ",
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

with st.expander("Data Sheet"):

    st.dataframe(data)

    csv = data.to_csv().encode('utf-8')

    

    st.download_button(
        label="Export data as CSV",
        data=csv,
        file_name='data_sheet.csv',
        mime='text/csv',
         )



imagem_referencia = st.file_uploader("Choose a pdf", type=["pdf"],accept_multiple_files=False)

if imagem_referencia is not None:

    agree = st.checkbox('Add to database')

button = st.button("Confirm")


if button and imagem_referencia is not None:
    with st.spinner('Please Wait'):
    

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
            st.error('Invoice Unkown, Please contact Konta.tech for better service ')













    


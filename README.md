"""

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
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<strong> Email : </strong> tahar.moumen@outlook.com </p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<strong> Tel : </strong> +212657497185 </p>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/tahar-moumen/)





"""

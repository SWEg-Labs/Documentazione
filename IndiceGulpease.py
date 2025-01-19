import textract
import os


def calcola_indice_gulpease(pdf_path):
    '''
    Calcolare l'indice di Leggibilita' di un PDF;
    Il codice crea un file csv 'RelazioneGulpease.csv' con la directory del file e l'indice di Gulpease;
    Sul terminale vengono stampate altre informazioni utili;
    '''
    
    print("------------------------------------------------------------")

    nf = pdf_path

    testo = textract.process(nf, method='pdftotext').decode('utf-8')

    #print(testo)

    import re
    parole  = len(re.findall(r'\w+', testo))
    lettere = len(re.findall(r'\w', testo))
    punti = len(re.findall(r'[.]+\s', testo))+len(re.findall(r'[;]+\s', testo)) - len(re.findall(r'[.]+\s+[.]', testo))

    indiceG=89+((300*punti)-(10*lettere))/parole
    print("numero di parole presenti nei doc :   " + str(parole))
    print("numero di lettere presenti nei doc :  " + str(lettere))
    print("numero di frasi presenti nei doc :    " + str(punti))
    print("")
    if parole!=0:
        if indiceG>100:
            indiceG=100

        print("indice di Gulpease restrittivo : " + str(indiceG))
        punti = len(re.findall('[.]', testo)) + len(re.findall('[;]', testo))
        indiceG = 89 + ((300 * punti) - (10 * lettere)) / parole
        if indiceG>100:
            indiceG=100

        print("indice di Gulpease non restrittivo : " + str(indiceG))
        print("")
        print("Nel primo indice non viene considerato delimitatore di frase:")
        print("- la punteggiatura spazio punteggiatura come delimitatore di frasi")
        print("- la punteggiatura che non e' seguita da un carattere di spaziatura")

        with open("RelazioneGulpease.csv", "a") as file:
            file.write(f"{nf},{round(indiceG,2)}\n")
    else:
        print("Errore nel calcolo dell'indice Gulpease")

    print("------------------------------------------------------------")


def find_pdfs_and_run_script(directory):
    ''''Funzione che cerca i pdf all'interno di una directory e per ciascun di essi esegue la funzione calcola_indice_gulpease'''

    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_path = os.path.join(root, file)
                calcola_indice_gulpease(pdf_path)


if __name__ == "__main__":
    directory = './output'  # Sostituisci con il percorso della directory che contiene i pdf fa valutare
    find_pdfs_and_run_script(directory)
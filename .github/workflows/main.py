"""
Script per compilare i documenti LaTex in PDF ed aggiornare il sito.

Dipendenze: python, latexmk.

Output:
- "index.html": pagina principale del sito;
- "website": directory contenente file utili al sito (e.g. css, immagini);
- "output": directory contenente i PDF compilati dai file latex.

Per funzionare correttamente lo script deve essere utilizzato nel seguente modo:
- Esecuzione: richiamare lo script dal terminale con il comando "python";
- Lo script deve essere contenuto in una directory del progetto;
- I file latex devono essere compilabili in PDF;
- Lo script termina con un OK finale (come ultimo messaggio), se non è così
potrebbero esserci stati dei problemi durante l'esecuzione.

È possibile utilizzare la sezione "MOD" per modificare la configurazione, in particolare:
- "PATH_DOCUMENTI: lista documenti tracciati;
- "PATH_VERBALI: directory dei verbali (vengono automaticamente compilati 
tutti i verbali presenti nella cartella).

Note:
- I percorsi sono composti utilizzando la funzione "os.path.join" per permettere 
l'esecuzione dello script su diversi sistemi operativi.

Problemi noti:
- In caso di errore o interruzione dell'esecuzione, lo script potrebbe lasciare dei 
file temporanei relativi alla compilazione dei file latex;
- [Windows] Lo script potrebbe fallire in caso di mancati permessi nella gestione dei file.
"""

import os
import shutil
from datetime import datetime
from zoneinfo import ZoneInfo




# --- Configurazione ---

# MOD: Configurazione modificabile
PATH_DOCUMENTI = [
    os.path.join("src", "template", "template.tex"),
    os.path.join("src", "PB", "Lettera di Presentazione", "lettera_presentazione.tex"),
    os.path.join("src", "PB", "Documentazione esterna", "Analisi dei Requisiti", "analisi_requisiti_v2.0.0.tex"),
    os.path.join("src", "PB", "Documentazione esterna", "Piano di Progetto", "piano_progetto_v2.0.0.tex"),
    os.path.join("src", "PB", "Documentazione esterna", "Piano di Qualifica", "piano_qualifica_v2.0.0.tex"),
    os.path.join("src", "PB", "Documentazione esterna", "Manuale Utente", "manuale_utente_v1.0.0.tex"),
    os.path.join("src", "PB", "Documentazione esterna", "Specifica Tecnica", "specifica_tecnica_v1.0.0.tex"),
    os.path.join("src", "PB", "Documentazione interna", "Glossario", "glossario_v2.0.0.tex"),
    os.path.join("src", "PB", "Documentazione interna", "Norme di Progetto", "norme_progetto_v2.0.0.tex"),
    os.path.join("src", "RTB", "Lettera di Presentazione", "lettera_presentazione.tex"),
    os.path.join("src", "RTB", "Documentazione esterna", "Analisi dei Requisiti", "analisi_requisiti_v1.0.0.tex"),
    os.path.join("src", "RTB", "Documentazione esterna", "Piano di Progetto", "piano_progetto_v1.0.0.tex"),
    os.path.join("src", "RTB", "Documentazione esterna", "Piano di Qualifica", "piano_qualifica_v1.0.0.tex"),
    os.path.join("src", "RTB", "Documentazione interna", "Glossario", "glossario_v1.0.0.tex"),
    os.path.join("src", "RTB", "Documentazione interna", "Norme di Progetto", "norme_progetto_v1.0.0.tex"),
    os.path.join("src", "Candidatura", "Lettera di Presentazione", "lettera_presentazione_v1.0.0.tex"),
    os.path.join("src", "Candidatura", "Preventivo dei costi ed impegni orari", "preventivo_impegni_v1.0.0.tex"),
    os.path.join("src", "Candidatura", "Valutazione dei Capitolati", "valutazione_capitolati_v1.0.0.tex")
    # I verbali non sono elencati in PATH_DOCUMENTI perchè sono tanti e quindi è più comodo listarli dalla cartella di origine
]
PATH_VERBALI_ESTERNI_PB = os.path.join("src", "PB", "Documentazione esterna", "Verbali esterni")
PATH_VERBALI_INTERNI_PB = os.path.join("src", "PB", "Documentazione interna", "Verbali interni")
PATH_VERBALI_ESTERNI_RTB = os.path.join("src", "RTB", "Documentazione esterna", "Verbali esterni")
PATH_VERBALI_INTERNI_RTB = os.path.join("src", "RTB", "Documentazione interna", "Verbali interni")
PATH_VERBALI_ESTERNI_CANDIDATURA = os.path.join("src", "Candidatura", "Verbali", "Verbali esterni")
PATH_VERBALI_INTERNI_CANDIDATURA = os.path.join("src", "Candidatura", "Verbali", "Verbali interni")

# Configurazione di default
NAME_OUTPUT_DIRECTORY = "output"
NAME_BASE_DIRECTORY = "Documentazione"   # Nome directory radice del progetto
PATH_WEBSITE_DIRECTORY = os.path.join(".github", "workflows")
PATH_BASE_DIRECTORY = ""  # Inizializzato in "set_path_base_directory"
PATH_OUTPUT = ""          # Inizializzato in "set_path_base_directory"
PATH_OUTPUT_TEMP = ""     # Inizializzato in "set_path_base_directory"

HTML_TEMPLATE_VERBALE = '<p><a href="<placeholder_link_verbale/>" target="_blank"><placeholder_titolo_verbale/></a></p>'




# --- Funzioni di Supporto ---

def get_output_file_path(path):
    list_path_elements = path.split(os.sep)

    if "PB" in list_path_elements:
        if "Documentazione esterna" in list_path_elements:
            if "Verbali esterni" in list_path_elements:
                return os.path.join(PATH_OUTPUT_TEMP, "PB", "Documentazione esterna", "Verbali esterni")
            return os.path.join(PATH_OUTPUT_TEMP, "PB", "Documentazione esterna")
        if "Documentazione interna" in list_path_elements:
            if "Verbali interni" in list_path_elements:
                return os.path.join(PATH_OUTPUT_TEMP, "PB", "Documentazione interna", "Verbali interni")
            return os.path.join(PATH_OUTPUT_TEMP, "PB", "Documentazione interna")
        return os.path.join(PATH_OUTPUT_TEMP, "PB")

    if "RTB" in list_path_elements:
        if "Documentazione esterna" in list_path_elements:
            if "Verbali esterni" in list_path_elements:
                return os.path.join(PATH_OUTPUT_TEMP, "RTB", "Documentazione esterna", "Verbali esterni")
            return os.path.join(PATH_OUTPUT_TEMP, "RTB", "Documentazione esterna")
        if "Documentazione interna" in list_path_elements:
            if "Verbali interni" in list_path_elements:
                return os.path.join(PATH_OUTPUT_TEMP, "RTB", "Documentazione interna", "Verbali interni")
            return os.path.join(PATH_OUTPUT_TEMP, "RTB", "Documentazione interna")
        return os.path.join(PATH_OUTPUT_TEMP, "RTB")

    if "Candidatura" in list_path_elements:
        if "Verbali" in list_path_elements:
            if "Verbali esterni" in list_path_elements:
                return os.path.join(PATH_OUTPUT_TEMP, "Candidatura", "Verbali", "Verbali esterni")
            return os.path.join(PATH_OUTPUT_TEMP, "Candidatura", "Verbali", "Verbali interni")
        return os.path.join(PATH_OUTPUT_TEMP, "Candidatura")
    
    return PATH_OUTPUT_TEMP

def compile_latex_and_move_pdf(name_file, path_directory):
    os.chdir(PATH_BASE_DIRECTORY)
    os.chdir(path_directory)
    os.system("latexmk -pdf " + name_file)
    # Ritorno alla cartella in caso di pacchetti latex mancanti
    os.chdir(PATH_BASE_DIRECTORY)
    os.chdir(path_directory)
    os.system("latexmk -c ")
    output_file_name = os.path.splitext(name_file)[0] + ".pdf"
    output_file_path = get_output_file_path(path_directory)
    shutil.move(output_file_name, os.path.join(output_file_path, output_file_name))
    os.chdir(PATH_BASE_DIRECTORY)

def get_website_html():
    try:
        file = open(os.path.join(PATH_WEBSITE_DIRECTORY, "index.html"), "r")
        file_content = file.read()
        return file_content
    finally:
        file.close()

def parse_month(number_month):
    months_map = {
        "01": "Gennaio",
        "02": "Febbraio",
        "03": "Marzo",
        "04": "Aprile",
        "05": "Maggio",
        "06": "Giugno",
        "07": "Luglio",
        "08": "Agosto",
        "09": "Settembre",
        "10": "Ottobre",
        "11": "Novembre",
        "12": "Dicembre",
    }
    if number_month in months_map:
        return months_map[number_month]

def parse_verbale_title(file_name):
    file_name_no_extension = os.path.splitext(file_name)[0]
    file_name_components = file_name_no_extension.split("_")
    
    date = file_name_components[2]
    date_components = date.split("-")
    
    day = date_components[0]
    month = parse_month(date_components[1])
    year = date_components[2]
    return day + " " + month + " 20" + year
    
def sort_by_date_desc(verbali_list):
    # Determine the prefix based on the first element
    if verbali_list[0].startswith('verbale_interno'):
        prefix = 'verbale_interno_'
    elif verbali_list[0].startswith('verbale_esterno'):
        prefix = 'verbale_esterno_'
    else:
        raise ValueError("The list must contain either internal or external minutes.") # minute = verbale

    # Define a function that extracts and converts the date to a datetime object
    def extract_date(verbale):
        # Remove prefix and extension, then convert to a datetime object
        date_str = verbale.replace(prefix, '').replace('.pdf', '')
        return datetime.strptime(date_str, '%d-%m-%y')
    
    # Sort the list using the extract_date function and reverse the order
    return sorted(verbali_list, key=extract_date, reverse=True)

def update_verbali(file_content):
    html_verbali_esterni_pb = ""
    html_verbali_interni_pb = ""
    html_verbali_esterni_rtb = ""
    html_verbali_interni_rtb = ""
    html_verbali_esterni_candidatura = ""
    html_verbali_interni_candidatura = ""


    # Verbali esterni PB

    file_verbali_list = os.listdir(os.path.join(PATH_OUTPUT, "PB", "Documentazione esterna", "Verbali esterni"))
        
    descending_order_file_verbali_list = sort_by_date_desc(file_verbali_list)
        
    for file_verbale in descending_order_file_verbali_list:
        html_verbali_esterni_pb += HTML_TEMPLATE_VERBALE.replace(
            "<placeholder_link_verbale/>", "output/PB/Documentazione esterna/Verbali esterni/" + file_verbale
        ).replace(
            "<placeholder_titolo_verbale/>", parse_verbale_title(file_verbale)
        ) + "\n"


    # Verbali interni PB

    file_verbali_list = os.listdir(os.path.join(PATH_OUTPUT, "PB", "Documentazione interna", "Verbali interni"))
        
    descending_order_file_verbali_list = sort_by_date_desc(file_verbali_list)
        
    for file_verbale in descending_order_file_verbali_list:
        html_verbali_interni_pb += HTML_TEMPLATE_VERBALE.replace(
            "<placeholder_link_verbale/>", "output/PB/Documentazione interna/Verbali interni/" + file_verbale
        ).replace(
            "<placeholder_titolo_verbale/>", parse_verbale_title(file_verbale)
        ) + "\n"
    
    
    # Verbali esterni RTB

    file_verbali_list = os.listdir(os.path.join(PATH_OUTPUT, "RTB", "Documentazione esterna", "Verbali esterni"))
        
    descending_order_file_verbali_list = sort_by_date_desc(file_verbali_list)
        
    for file_verbale in descending_order_file_verbali_list:
        html_verbali_esterni_rtb += HTML_TEMPLATE_VERBALE.replace(
            "<placeholder_link_verbale/>", "output/RTB/Documentazione esterna/Verbali esterni/" + file_verbale
        ).replace(
            "<placeholder_titolo_verbale/>", parse_verbale_title(file_verbale)
        ) + "\n"


    # Verbali interni RTB

    file_verbali_list = os.listdir(os.path.join(PATH_OUTPUT, "RTB", "Documentazione interna", "Verbali interni"))
        
    descending_order_file_verbali_list = sort_by_date_desc(file_verbali_list)
        
    for file_verbale in descending_order_file_verbali_list:
        html_verbali_interni_rtb += HTML_TEMPLATE_VERBALE.replace(
            "<placeholder_link_verbale/>", "output/RTB/Documentazione interna/Verbali interni/" + file_verbale
        ).replace(
            "<placeholder_titolo_verbale/>", parse_verbale_title(file_verbale)
        ) + "\n"
    

    # Verbali esterni Candidaura

    file_verbali_list = os.listdir(os.path.join(PATH_OUTPUT, "Candidatura", "Verbali", "Verbali esterni"))
        
    descending_order_file_verbali_list = sort_by_date_desc(file_verbali_list)
        
    for file_verbale in descending_order_file_verbali_list:
        html_verbali_esterni_candidatura += HTML_TEMPLATE_VERBALE.replace(
            "<placeholder_link_verbale/>", "output/Candidatura/Verbali/Verbali esterni/" + file_verbale
        ).replace(
            "<placeholder_titolo_verbale/>", parse_verbale_title(file_verbale)
        ) + "\n"


    # Verbali interni Candidaura

    file_verbali_list = os.listdir(os.path.join(PATH_OUTPUT, "Candidatura", "Verbali", "Verbali interni"))
        
    descending_order_file_verbali_list = sort_by_date_desc(file_verbali_list)
        
    for file_verbale in descending_order_file_verbali_list:
        html_verbali_interni_candidatura += HTML_TEMPLATE_VERBALE.replace(
            "<placeholder_link_verbale/>", "output/Candidatura/Verbali/Verbali interni/" + file_verbale
        ).replace(
            "<placeholder_titolo_verbale/>", parse_verbale_title(file_verbale)
        ) + "\n"


    file_content_updated = file_content\
        .replace("<placeholder_verbali_esterni_pb/>", html_verbali_esterni_pb)\
        .replace("<placeholder_verbali_interni_pb/>", html_verbali_interni_pb)\
        .replace("<placeholder_verbali_esterni_rtb/>", html_verbali_esterni_rtb)\
        .replace("<placeholder_verbali_interni_rtb/>", html_verbali_interni_rtb)\
        .replace("<placeholder_verbali_esterni_candidatura/>", html_verbali_esterni_candidatura)\
        .replace("<placeholder_verbali_interni_candidatura/>", html_verbali_interni_candidatura)
        
    return file_content_updated

def update_last_update_date(html_website):
    italy_tz = ZoneInfo("Europe/Rome")
    italian_time = datetime.now(italy_tz)
    time_string = italian_time.strftime("%d/%m/%Y %H:%M")
    return html_website.replace("<placeholder_last_update/>", "Ultimo aggiornamento: " + time_string)




# --- Funzioni Primarie ---

def set_path_base_directory():
    """
    Termina la configurazione di: 
    - PATH_BASE_DIRECTORY: percorso della directory principale, specificata in NAME_BASE_DIRECTORY; 
    - PATH_OUTPUT: percorso della directory di output dei PDF;
    - PATH_OUTPUT_TEMP: percorso della directory di output dei PDF temporanea.
    Inoltre imposta la directory corrente a PATH_BASE_DIRECTORY, per permettere consistenza
    con i comandi invocati successivamente.
    """
    file_path = os.path.realpath(__file__)
    file_path_list = file_path.split(os.sep)
    found_path = False
    while not found_path:
        if file_path_list[-1] == NAME_BASE_DIRECTORY:
            found_path = True
        else:
            file_path_list.pop()
    global PATH_BASE_DIRECTORY, PATH_OUTPUT, PATH_OUTPUT_TEMP
    PATH_BASE_DIRECTORY = os.sep.join(file_path_list)
    PATH_OUTPUT = os.path.join(PATH_BASE_DIRECTORY, NAME_OUTPUT_DIRECTORY)
    PATH_OUTPUT_TEMP = os.path.join(PATH_BASE_DIRECTORY, "temp_" + NAME_OUTPUT_DIRECTORY)
    os.chdir(PATH_BASE_DIRECTORY)

def clean_start():
    """
    Rimuove, se esistenti, i file relativi al sito: 'index.html', 'website/'
    """
    if os.path.exists("index.html"):
        os.remove("index.html")
    if os.path.exists("website"):
        shutil.rmtree("website")

def create_new_output_directory():
    """
    Crea una directory temporanea in cui mettere i PDF generati.
    """
    if os.path.exists(PATH_OUTPUT_TEMP):
        shutil.rmtree(PATH_OUTPUT_TEMP)
    os.mkdir(PATH_OUTPUT_TEMP)

    os.mkdir(os.path.join(PATH_OUTPUT_TEMP, "PB"))
    os.mkdir(os.path.join(PATH_OUTPUT_TEMP, "PB", "Documentazione esterna"))
    os.mkdir(os.path.join(PATH_OUTPUT_TEMP, "PB", "Documentazione esterna", "Verbali esterni"))
    os.mkdir(os.path.join(PATH_OUTPUT_TEMP, "PB", "Documentazione interna"))
    os.mkdir(os.path.join(PATH_OUTPUT_TEMP, "PB", "Documentazione interna", "Verbali interni"))

    os.mkdir(os.path.join(PATH_OUTPUT_TEMP, "RTB"))
    os.mkdir(os.path.join(PATH_OUTPUT_TEMP, "RTB", "Documentazione esterna"))
    os.mkdir(os.path.join(PATH_OUTPUT_TEMP, "RTB", "Documentazione esterna", "Verbali esterni"))
    os.mkdir(os.path.join(PATH_OUTPUT_TEMP, "RTB", "Documentazione interna"))
    os.mkdir(os.path.join(PATH_OUTPUT_TEMP, "RTB", "Documentazione interna", "Verbali interni"))

    os.mkdir(os.path.join(PATH_OUTPUT_TEMP, "Candidatura"))
    os.mkdir(os.path.join(PATH_OUTPUT_TEMP, "Candidatura", "Verbali"))
    os.mkdir(os.path.join(PATH_OUTPUT_TEMP, "Candidatura", "Verbali", "Verbali esterni"))
    os.mkdir(os.path.join(PATH_OUTPUT_TEMP, "Candidatura", "Verbali", "Verbali interni"))

def latex_to_pdf():
    """
    Compila i documenti latex e li sposta nella directory di output.
    """
    for path_file in PATH_DOCUMENTI:
        if os.path.exists(path_file):
            path_directory, name_file = os.path.split(path_file)
            compile_latex_and_move_pdf(name_file, path_directory)

    if os.path.exists(PATH_VERBALI_ESTERNI_PB):
        list_directory_verbale = os.listdir(PATH_VERBALI_ESTERNI_PB)
        for directory_verbale in list_directory_verbale:
            path_directory = os.path.join(PATH_VERBALI_ESTERNI_PB, directory_verbale)
            name_file = directory_verbale + ".tex"
            compile_latex_and_move_pdf(name_file, path_directory)

    if os.path.exists(PATH_VERBALI_INTERNI_PB):
        list_directory_verbale = os.listdir(PATH_VERBALI_INTERNI_PB)
        for directory_verbale in list_directory_verbale:
            path_directory = os.path.join(PATH_VERBALI_INTERNI_PB, directory_verbale)
            name_file = directory_verbale + ".tex"
            compile_latex_and_move_pdf(name_file, path_directory)
            
    if os.path.exists(PATH_VERBALI_ESTERNI_RTB):
        list_directory_verbale = os.listdir(PATH_VERBALI_ESTERNI_RTB)
        for directory_verbale in list_directory_verbale:
            path_directory = os.path.join(PATH_VERBALI_ESTERNI_RTB, directory_verbale)
            name_file = directory_verbale + ".tex"
            compile_latex_and_move_pdf(name_file, path_directory)

    if os.path.exists(PATH_VERBALI_INTERNI_RTB):
        list_directory_verbale = os.listdir(PATH_VERBALI_INTERNI_RTB)
        for directory_verbale in list_directory_verbale:
            path_directory = os.path.join(PATH_VERBALI_INTERNI_RTB, directory_verbale)
            name_file = directory_verbale + ".tex"
            compile_latex_and_move_pdf(name_file, path_directory)
            
    if os.path.exists(PATH_VERBALI_ESTERNI_CANDIDATURA):
        list_directory_verbale = os.listdir(PATH_VERBALI_ESTERNI_CANDIDATURA)
        for directory_verbale in list_directory_verbale:
            path_directory = os.path.join(PATH_VERBALI_ESTERNI_CANDIDATURA, directory_verbale)
            name_file = directory_verbale + ".tex"
            compile_latex_and_move_pdf(name_file, path_directory)
        
    if os.path.exists(PATH_VERBALI_INTERNI_CANDIDATURA):
        list_directory_verbale = os.listdir(PATH_VERBALI_INTERNI_CANDIDATURA)
        for directory_verbale in list_directory_verbale:
            path_directory = os.path.join(PATH_VERBALI_INTERNI_CANDIDATURA, directory_verbale)
            name_file = directory_verbale + ".tex"
            compile_latex_and_move_pdf(name_file, path_directory)
        
def replace_old_output_directory():
    """
    Sostituisce la directory con i file PDF generati recentemente con quella già esistente, se presente.
    """
    if os.path.exists(PATH_OUTPUT):
        shutil.rmtree(PATH_OUTPUT)
    os.rename(PATH_OUTPUT_TEMP, PATH_OUTPUT)
        
def generate_website():
    """
    Genera il sito, aggiornando la sezione verbali e aggiornando la data di "last update".
    """
    html_template_website = get_website_html()
    html_updated_website = update_verbali(html_template_website)
    html_updated_website = update_last_update_date(html_updated_website)
    try:
        file = open("index.html", "w")
        file.write(html_updated_website)
        shutil.copytree(os.path.join(PATH_WEBSITE_DIRECTORY, "website"), "website")
    finally:
        file.close()

def ok_message():
    """
    Stampa un messaggio per segnalare la corretta terminazione dello script.
    """
    print("\n[" + os.path.basename(__file__) + "] OK\n")
  
  
  

# --- Main ---

def main():
    set_path_base_directory()
    clean_start()

    create_new_output_directory()
    latex_to_pdf()
    replace_old_output_directory()
  
    generate_website()

    ok_message()

if __name__ == "__main__":
    main()


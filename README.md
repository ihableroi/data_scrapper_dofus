Ce code (code_beta.py)permet l'extraction de tous les prix de tous les items (ressources, consommables, équipements) des HDV de dofus retro, et les stock dans un fichier CSV. 
Ensuite, le code (analyseur.py) permet de calculer la rentabilité des crafts à partir de ce fichier CSV, en produisant un deuxieme fichier CSV.

j'ai utilisé les librairies Tesseract, CSV, pyautogui et ctypes.

Le code doit être réadapté à votre résolution d'écran.

Le code est plutôt robuste et dispose de moyens de contourner plusieurs limittations des fonctions de l'OCR TESSERACT.

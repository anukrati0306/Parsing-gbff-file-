import os
import re
import tqdm
import pandas as pd
# os.path.join(file, "hello.txt")
# tqdm for progress bar
# use beautiful soup to download files
# unzip using python loops
import shutil

for folder_name in ["exception", "output", "errors"]:
    shutil.rmtree(folder_name, ignore_errors=True)
    os.mkdir(folder_name)

def write_output(file):
    with open("fungi/"+file) as f:
        data = f.read()
    csv_dict = []
    all_species = data.split("//")
    for idx, specie in enumerate(tqdm.tqdm(all_species[:-1])):
        try:
            species_dict = {}
            first_translation_character = re.findall('''translation="(.)''', specie)[0]
            locus_id = re.findall('''LOCUS\s+([A-Z_\d]*)''', specie)[0]
            comment = re.findall('''COMMENT\s+([^\:]*)''', specie)[0]
            cds = re.findall('''CDS\s+([<>\d.]*)''', specie)[0].split(" ")[-1]
            origin_with_numbers_and_space = re.findall('''ORIGIN(.*)''', specie, re.DOTALL)[0]
            origin = re.sub(r'[^a-zA-Z]+', '', origin_with_numbers_and_space)
            starting_idx_for_origin = int(cds.split(".")[0])-1
            origin = origin[starting_idx_for_origin:starting_idx_for_origin+3]
            if (origin == "atg" and first_translation_character != "M" and "<" not in cds):
                with open("exception/" + file + "_exception.txt", "a") as k:
                    k.write("idx: %s has origin == atg but first_translation_character is not M \n\n" %(idx))
            if (first_translation_character=="M" and origin != "atg" and "<" not in cds):
                with open("exception/" + file + "_exception.txt", "a") as k:
                    k.write("idx: %s has origin != atg but first_translation_character is M \n\n" %(idx))
            species_dict
            species_dict["idx"] = str(idx)
            species_dict["first_translation_character"] = first_translation_character
            species_dict["locus_id"] = locus_id
            species_dict["comment"] = comment
            species_dict["cds"] = cds
            species_dict["origin"] = origin
            csv_dict.append(species_dict)
        except Exception as e:
            with open("errors/errors.txt", "a") as f:
                f.write("failed at idx: %s due to %s" %(idx, e))
                f.write("\n\n")
    df = pd.DataFrame.from_dict(csv_dict)
    df.to_csv("output/output.csv", index = False)

for file in os.listdir("fungi"):
    write_output(file)
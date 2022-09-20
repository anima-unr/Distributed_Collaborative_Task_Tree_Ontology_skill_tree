Files used to generate new YAML files!

How to run them:

1) python parse_task_tree.py (you will need to edit string and string2 on line 172 & 181 to fit the structure of the tree)
2) copy the output from the terminal from "PARSE STR" up to "XXXXXX..XX" and paste into output.txt (it should save to this file, but for some reason it saves it weirdly... should fix this at some point)
3) python reorder.py (this will save the yaml file to output.yaml)

Then you have your new yaml file! May need to edit it for styling purposes.

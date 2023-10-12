import os
import subprocess
from typing import List
from conllup.conllup import readConlluFile
import json

PATH_TESTS_DESCRIPTION = "./tests_description.json"

RULE_TO_CHECK = "zh_mSUD_to_SUD"

PATH_DATA_FOLDER = './data/'


class TestDescription:
    TEST_FOLDER_NAME: str
    GRS_FILE: str
    CONFIG_TYPE: str
    STRAT_NAME: str



def _load_tests_description() -> List[TestDescription]:
    with open(PATH_TESTS_DESCRIPTION, "r") as f:
        tests_description = json.load(f)
    return tests_description

def print_red(text):
    print("\033[91m" + text + "\033[0m")

def diff_json(json1, json2, path=""):
    for key in json1.keys():
        if key not in json2:
            print_red(f"{path}{key} in first JSON only")
        else:
            if isinstance(json1[key], dict) and isinstance(json2[key], dict):
                diff_json(json1[key], json2[key], path + key + ".")
            elif json1[key] != json2[key]:
                print_red(f"{path}{key} differ: {json1[key]} != {json2[key]}")
    
    for key in json2.keys():
        if key not in json1:
            print_red(f"{path}{key} in second JSON only")


def test_sentence_lengths(path_expected: str, path_converted: str):
    expected_sentences = readConlluFile(path_expected)
    converted_sentences = readConlluFile(path_converted)

    if len(expected_sentences) != len(converted_sentences):
        print_red(f"Expected {len(expected_sentences)} sentences, but got {len(converted_sentences)} sentences in converted.")


def test_sentences_individually(path_expected: str, path_converted: str):
    expected_sentences = readConlluFile(path_expected)
    converted_sentences = readConlluFile(path_converted)

    # Check each individual sentence for length equality
    for i, (expected, converted) in enumerate(zip(expected_sentences, converted_sentences)):
        if len(expected) != len(converted):
            print_red(f"Sentence {i+1} has length {len(expected)} in expected, but {len(converted)} in converted.")
            continue
        
        expected_meta = expected["metaJson"]
        converted_meta = converted["metaJson"]

        if expected_meta != converted_meta:
            print_red(f"Sentence {i+1} has different metadata in expected and converted.")
            diff_json(expected_meta, converted_meta)


        expected_id = expected_meta["sent_id"]
        converted_id = converted_meta["sent_id"]

        expected_nodes = expected["treeJson"]["nodesJson"]
        converted_nodes = converted["treeJson"]["nodesJson"]

        expected_nodes_forms = [node["FORM"] for node in expected_nodes.values()]
        converted_nodes_forms = [node["FORM"] for node in converted_nodes.values()]
        if len(expected_nodes) != len(converted_nodes):
            print_red(f"Sentence {i+1} (sent_id = {expected_id}) has different number of nodes in expected and converted.\nexpected_nodes_form = {expected_nodes_forms}\nconverted_nodes_form = {converted_nodes_forms}", end="\n\n")
            continue

        for j, (expected_node, converted_node) in enumerate(zip(expected_nodes.values(), converted_nodes.values())):
            expected_node_str = json.dumps(expected_node, ensure_ascii=False)
            converted_node_str = json.dumps(converted_node, ensure_ascii=False)
            if expected_node != converted_node:
                # this show both nodes in json format
                print_red(f"Sentence {i+1} (sent_id = {expected_id}) has different nodes (ID = {expected_node['ID']}).\nexpected_node = {expected_node_str}\nconverted_node = {converted_node_str}")
                # this show only the different fields
                diff_json(expected_node, converted_node)
                print()


if __name__ == "__main__":
    tests_description_json = _load_tests_description()
    for test_description in tests_description_json:
        TEST_FOLDER_NAME = test_description["TEST_FOLDER_NAME"]
        GRS_FILE = test_description["GRS_FILE"]
        CONFIG_TYPE = test_description["CONFIG_TYPE"]
        STRAT_NAME = test_description["STRAT_NAME"]
        
        print("DOING TEST :", TEST_FOLDER_NAME)
        path_conlls_folder = os.path.join(PATH_DATA_FOLDER, TEST_FOLDER_NAME)

        path_source = os.path.join(path_conlls_folder, "source.conllu")
        path_converted = os.path.join(path_conlls_folder, "converted.conllu")
        path_expected = os.path.join(path_conlls_folder, "expected.conllu")
        
        print("CONVERTING...")
        cmd = f'opam exec -- grew transform -grs ../grs/{GRS_FILE} -config {CONFIG_TYPE} -i {path_source} -o {path_converted} -strat {STRAT_NAME}'
        print("$", cmd)
        result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
        if result.returncode != 0:
            print_red("ERROR IN GREW CONVERSION")
            print_red(result.stderr)
            continue

        test_sentence_lengths(path_expected, path_converted)
        test_sentences_individually(path_expected, path_converted)
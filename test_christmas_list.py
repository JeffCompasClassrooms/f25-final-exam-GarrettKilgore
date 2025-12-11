import pytest
import os
import tempfile
import shutil
import pickle
from christmas_list import ChristmasList


def describe_ChristmasList_System_Tests():
    
    @pytest.fixture
    def temp_dir():
        test_dir = tempfile.mkdtemp()
        yield test_dir
        shutil.rmtree(test_dir, ignore_errors=True)
    
    @pytest.fixture
    def test_file(temp_dir):
        return os.path.join(temp_dir, "test_christmas_list.pkl")
    
    @pytest.fixture
    def christmas_list(test_file):
        return ChristmasList(test_file)
    

    def describe_loadItems_functionality():
        
        def it_loads_empty_list(christmas_list):
            christmas_list.saveItems([])
            items = christmas_list.loadItems()
            assert items == []
            assert isinstance(items, list)
        
        def it_loads_single_item(christmas_list):
            test_data = [{"name": "puzzle", "purchased": True}]
            christmas_list.saveItems(test_data)
            items = christmas_list.loadItems()
            assert len(items) == 1
            assert items[0]["name"] == "puzzle"
            assert items[0]["purchased"] == True
        
        def it_loads_multiple_items(christmas_list):
            test_data = [
                {"name": "doll", "purchased": False},
                {"name": "truck", "purchased": True},
                {"name": "ball", "purchased": False}
            ]
            christmas_list.saveItems(test_data)
            items = christmas_list.loadItems()
            assert len(items) == 3
            assert items[0]["name"] == "doll"
            assert items[1]["purchased"] == True
            assert items[2]["name"] == "ball"


    def describe_saveItems_functionality():
        
        def it_saves_empty_list(christmas_list, test_file):
            christmas_list.saveItems([])
            assert os.path.exists(test_file)
            with open(test_file, "rb") as f:
                items = pickle.load(f)
            assert items == []
        
        def it_saves_single_item(christmas_list, test_file):
            test_items = [{"name": "robot", "purchased": False}]
            christmas_list.saveItems(test_items)
            with open(test_file, "rb") as f:
                items = pickle.load(f)
            assert len(items) == 1
            assert items[0]["name"] == "robot"
            assert items[0]["purchased"] == False
        
        def it_saves_multiple_items(christmas_list, test_file):
            test_items = [{"name": "skateboard", "purchased": False},
                          {"name": "helmet", "purchased": True},
                          {"name": "knee pads", "purchased": False}
                          ]
            christmas_list.saveItems(test_items)
            with open(test_file, "rb") as f:
                items = pickle.load(f)
            assert len(items) == 3
            assert items[0]["name"] == "skateboard"
            assert items[1]["purchased"] == True
            assert items[2]["name"] == "knee pads"
    
    def describe_add_functionality():
        
        def it_adds_single_item(christmas_list):
            christmas_list.add("bb gun")
            items = christmas_list.loadItems()
            assert len(items) == 1
            assert items[0]["name"] == "bb gun"
            assert items[0]["purchased"] == False
        
        def it_adds_multiple_items(christmas_list):
            christmas_list.add("bike")
            christmas_list.add("toy train")
            christmas_list.add("teddy bear")
            items = christmas_list.loadItems()
            assert len(items) == 3
            assert items[0]["name"] == "bike"
            assert items[1]["name"] == "toy train"
            assert items[2]["name"] == "teddy bear"
        
        def it_allows_duplicate_names(christmas_list):
            christmas_list.add("toy car")
            christmas_list.add("toy car")
            items = christmas_list.loadItems()
            assert len(items) == 2
            assert all(item["name"] == "toy car" for item in items)
    
    def describe_check_off_functionality():
        
        def check_off_work_in_print_list(christmas_list, capsys):
            christmas_list.add("bb gun")
            christmas_list.check_off("bb gun")
            christmas_list.print_list()
            captured = capsys.readouterr()
            assert captured.out == "[x] bb gun\n"
    
    
    def describe_remove_functionality():
        
        def it_removes_single_item(christmas_list):
            christmas_list.add("yo-yo")
            christmas_list.remove("yo-yo")
            items = christmas_list.loadItems()
            assert len(items) == 0
        
        def it_removes_specific_item_from_multiple(christmas_list):
            christmas_list.add("blocks")
            christmas_list.add("crayons")
            christmas_list.add("paint")
            christmas_list.remove("crayons")
            items = christmas_list.loadItems()
            assert len(items) == 2
            assert items[0]["name"] == "blocks"
            assert items[1]["name"] == "paint"
        
        def it_removes_all_matching_duplicates(christmas_list):
            christmas_list.add("cookie")
            christmas_list.add("cookie")
            christmas_list.add("cake")
            christmas_list.remove("cookie")
            items = christmas_list.loadItems()
            assert len(items) == 1
            assert items[0]["name"] == "cake"
        
        def it_handles_removing_nonexistent_item(christmas_list):
            christmas_list.add("book")
            christmas_list.remove("nonexistent") 
            items = christmas_list.loadItems()
            assert len(items) == 1
            assert items[0]["name"] == "book"
    
    
    def describe_print_list_functionality():
        
        def it_prints_empty_list(christmas_list, capsys):
            christmas_list.print_list()
            captured = capsys.readouterr()
            assert captured.out == ""
        
        def it_prints_unchecked_item(christmas_list, capsys):
            christmas_list.add("bb gun")
            christmas_list.print_list()
            captured = capsys.readouterr()
            assert captured.out == "[_] bb gun\n"
        
        def it_prints_checked_item(christmas_list, capsys):
            christmas_list.add("bb gun")
            christmas_list.check_off("bb gun")
            christmas_list.print_list()
            captured = capsys.readouterr()
            assert captured.out == "[x] bb gun\n"
        
        def it_prints_multiple_items_mixed_status(christmas_list, capsys):
            christmas_list.add("telescope")
            christmas_list.add("microscope")
            christmas_list.add("compass")
            christmas_list.check_off("microscope")
            christmas_list.print_list()
            captured = capsys.readouterr()
            expected = "[_] telescope\n[x] microscope\n[_] compass\n"
            assert captured.out == expected
    
    def describe_edge_cases():
        
        def it_handles_empty_string_name(christmas_list):
            christmas_list.add("")
            items = christmas_list.loadItems()
            assert len(items) == 1
            assert items[0]["name"] == ""
        
        def it_handles_special_characters_in_name(christmas_list):
            special_name = "toy $5.99"
            christmas_list.add(special_name)
            items = christmas_list.loadItems()
            assert items[0]["name"] == special_name
        
        def it_handles_very_long_name(christmas_list):
            long_name = "a" * 1000
            christmas_list.add(long_name)
            items = christmas_list.loadItems()
            assert items[0]["name"] == long_name
        
        def it_handles_unicode_characters(christmas_list):
            christmas_list.add("Christmas Tree")
            christmas_list.add("Snowman")
            items = christmas_list.loadItems()
            assert len(items) == 2
            assert items[0]["name"] == "Christmas Tree"
            assert items[1]["name"] == "Snowman"
        
        def it_handles_newlines_in_name(christmas_list):
            christmas_list.add("multi\nline\nitem")
            items = christmas_list.loadItems()
            assert items[0]["name"] == "multi\nline\nitem"
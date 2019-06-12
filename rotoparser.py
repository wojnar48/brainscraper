import csv
import json

from schemas import player_schema, player_headers

class RotoPlayerParser(object):
    """
        TODO(SW): Include nested list fields once data is saved to DB.
    """

    NESTED = dict()

    def __init__(self, player_type, date_str, data, schema):
        data = RotoPlayerParser.load_data(data)
        self.data = RotoPlayerParser.transform_data(data)

        self.schema = schema
        self.player_type = player_type
        self.date_str = date_str

    @classmethod
    def clean_data(cls, data):
        return [item for item in data if isinstance(item, dict)]
    
    @classmethod
    def load_data(cls, data):
        return cls.clean_data(json.loads(data))
        
    @classmethod
    def transform_data(cls, data):
        transformed = dict()

        for item in data:
            if isinstance(item, dict):
                sub_item = dict()
                for key, val in item.items():
                    if isinstance(val, list):
                        # TODO(SW): Save elements to DB once implemented
                        cls.NESTED[f'{key}__{len(cls.NESTED.keys())}'] = val
                    elif isinstance(val, dict):
                        for k, v in val.items():
                            cls.build_nested_keys(sub_item, f'{key}__{k}', v)
                    elif isinstance(key, str) and type(val) in [int, float, str, bool, type(None)]:
                        sub_item[key] = val
                    else:
                        print(f'Invalid data type for key={key}, val={val}')

                transformed[item.get('player_name')] = sub_item
        return transformed

    @classmethod
    def build_nested_keys(cls, parent_item, parent_key, item):
        if not isinstance(parent_key, str):
            return

        # disregard list items until we have a DB
        if isinstance(item, list):
            return

        # if the parent has a valid key but item is None
        if isinstance(parent_key, str) and type(item) not in [int, float, str]:
            parent_item[parent_key] = 'NA'
            return

        # if instance of dict get k, v and recurse
        if isinstance(item, dict):
            for key, val in item.items():
                cls.build_nested_keys(parent_item, f'{parent_key}__{key}', val)
        else:
            parent_item[parent_key] = item
               
 
    def to_csv(self):
        with open(f'output/{self.date_str}_{self.player_type}.csv', 'w') as csv_file:
            writer = csv.DictWriter(csv_file, extrasaction='ignore', fieldnames=player_headers)
            
            writer.writeheader()
            for pname, player in self.data.items():
                print(f'Processing player: {pname}')
                writer.writerow(player)
        
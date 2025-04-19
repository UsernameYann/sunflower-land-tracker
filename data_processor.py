import os
import json

class DataProcessor:
    COLORS = {
        'coins': (242/255, 177/255, 79/255, 1),
        'Gem': (151/255, 228/255, 237/255, 1),
        'FLOWER': (255/255, 182/255, 193/255, 1),
        'Mark': (194/255, 203/255, 218/255, 1),
        'Love Charm': (220/255, 20/255, 60/255, 1),
        'Sunflower': (254/255, 249/255, 110/255, 1),
        'Potato': (202/255, 123/255, 78/255, 1),
        'Rhubarb': (200/255, 50/255, 80/255, 1),
        'Pumpkin': (231/255, 125/255, 59/255, 1),
        'Zucchini': (50/255, 120/255, 50/255, 1),
        'Carrot': (242/255, 177/255, 79/255, 1),
        'Yam': (255/255, 130/255, 60/255, 1),
        'Cabbage': (230/255, 124/255, 125/255, 1),
        'Broccoli': (100/255, 160/255, 80/255, 1),
        'Soybean': (82/255, 135/255, 79/255, 1),
        'Beetroot': (169/255, 86/255, 134/255, 1),
        'Pepper': (200/255, 30/255, 30/255, 1),
        'Cauliflower': (224/255, 185/255, 155/255, 1),
        'Parsnip': (230/255, 213/255, 175/255, 1),
        'Eggplant': (98/255, 99/255, 132/255, 1),
        'Corn': (239/255, 175/255, 78/255, 1),
        'Onion': (150/255, 60/255, 90/255, 1),
        'Radish': (208/255, 73/255, 73/255, 1),
        'Wheat': (247/255, 221/255, 80/255, 1),
        'Turnip': (255/255, 140/255, 160/255, 1),
        'Kale': (82/255, 135/255, 79/255, 1),
        'Artichoke': (220/255, 190/255, 255/255, 1),
        'Barley': (202/255, 123/255, 78/255, 1),
        'Tomato': (203/255, 71/255, 71/255, 1),
        'Lemon': (241/255, 231/255, 171/255, 1),
        'Blueberry': (44/255, 94/255, 193/255, 1),
        'Orange': (232/255, 168/255, 67/255, 1),
        'Apple': (149/255, 49/255, 55/255, 1),
        'Banana': (250/255, 232/255, 119/255, 1),
        'Wild Mushroom': (255/255, 99/255, 132/255, 1),
        'Magic Mushroom': (255/255, 206/255, 86/255, 1),
        'Grape': (75/255, 192/255, 192/255, 1),
        'Rice': (153/255, 102/255, 255/255, 1),
        'Olive': (255/255, 159/255, 64/255, 1),
        'Egg': (255/255, 206/255, 86/255, 1),
        'Honey': (255/255, 99/255, 132/255, 1),
        'Leather': (54/255, 162/255, 235/255, 1),
        'Wool': (75/255, 192/255, 192/255, 1),
        'Merino Wool': (153/255, 102/255, 255/255, 1),
        'Feather': (194/255, 203/255, 218/255, 1),
        'Milk': (142/255, 155/255, 178/255, 1),
        'Wood': (174/255, 114/255, 86/255, 1),
        'Stone': (142/255, 155/255, 178/255, 1),
        'Iron': (200/255, 207/255, 204/255, 1),
        'Gold': (241/255, 224/255, 128/255, 1),
        'Crimstone': (203/255, 51/255, 43/255, 1),
        'Sunstone': (255/255, 251/255, 0/255, 1),
        'Oil': (40/255, 40/255, 40/255, 1),
        'Sprout Mix': (2/255, 128/255, 2/255, 1),
        'Fruitful Blend': (178/255, 34/255, 34/255, 1),
        'Rapid Root': (0, 0, 0.8, 1),
        'Earthworm': ((163/255, 101/255, 84/255, 1)),
        'Grub': (133/255, 94/255, 66/255, 1),
        'Red Wiggler': (165/255, 60/255, 53/255, 1)
    }

    CATEGORIES = {
        'Balance': {
            'name': "Balance",
            'items': ['coins', 'Gem', 'FLOWER', 'Love Charm', 'Mark']
        },
        'basicCrops': {
            'name': "Basic Vegetables",
            'items': ['Sunflower', 'Potato', 'Rhubarb', 'Pumpkin', 'Zucchini',]
        },
        'mediumCrops': {
            'name': "Medium Vegetables",
            'items': ['Carrot', 'Yam', 'Cabbage', 'Broccoli', 'Soybean', 'Beetroot', 'Pepper', 'Cauliflower', 'Parsnip']
        },
        'advancedCrops': {
            'name': "Advanced Vegetables",
            'items': ['Eggplant', 'Corn', 'Onion', 'Radish', 'Wheat', 'Turnip', 'Kale', 'Artichoke', 'Barley']
        },
        'fruits': {
            'name': "Fruits",
            'items': ['Tomato', 'Lemon', 'Blueberry', 'Orange', 'Apple', 'Banana']
        },
        'Mushroom': {
            'name': "Mushrooms",
            'items': ['Wild Mushroom', 'Magic Mushroom']
        },
        'greenhouse': {
            'name': "Greenhouses",
            'items': ['Grape', 'Rice', 'Olive']
        },
        'Animals': {
            'name': "Animals",
            'items': ['Egg', 'Honey', 'Leather', 'Wool', 'Merino Wool', 'Feather', 'Milk']
        },
        'resources': {
            'name': "Resources",
            'items': ['Wood', 'Stone', 'Iron', 'Gold', 'Crimstone', 'Sunstone', 'Oil']
        },
        'composters': {
            'name': "Composters",
            'items': ['Rapid Root', 'Fruitful Blend', 'Sprout Mix', 'Earthworm', 'Grub', 'Red Wiggler']
        }
    }

    def __init__(self, base_dir="data"):
        self.base_dir = base_dir

    def get_user_data(self, user_id):
        if hasattr(self, '_cached_user_id') and self._cached_user_id == user_id and hasattr(self, '_cached_data'):
            return self._cached_data
            
        user_dir = os.path.join(self.base_dir, str(user_id))
        if not os.path.exists(user_dir):
            return None, None

        data_series = {cat: {item: [] for item in self.CATEGORIES[cat]['items']} 
                      for cat in self.CATEGORIES}
        dates = []

        for filename in sorted(os.listdir(user_dir)):
            if filename.endswith('.json'):
                with open(os.path.join(user_dir, filename), 'r') as f:
                    data = json.load(f)
                    dates.append(filename.replace('.json', ''))
                    
                    farm_data = data.get('farm', {})
                    inventory = farm_data.get('inventory', {})

                    data_series['Balance']['coins'].append(float(farm_data.get('coins', 0)))
                    data_series['Balance']['FLOWER'].append(float(farm_data.get('balance', 0)))
                    gem_value = inventory.get('Gem', '0')
                    try:
                        gem_value = float(gem_value)
                    except (ValueError, TypeError):
                        gem_value = 0
                    data_series['Balance']['Gem'].append(gem_value)
                    
                    mark_value = inventory.get('Mark', '0')
                    try:
                        mark_value = float(mark_value)
                    except (ValueError, TypeError):
                        mark_value = 0
                    data_series['Balance']['Mark'].append(mark_value)

                    love_charm_value = inventory.get('Love Charm', '0')
                    try:
                        love_charm_value = float(love_charm_value)
                    except (ValueError, TypeError):
                        love_charm_value = 0
                    data_series['Balance']['Love Charm'].append(love_charm_value)

                    for category in self.CATEGORIES:
                        if category != 'Balance':
                            for item in self.CATEGORIES[category]['items']:
                                value = inventory.get(item, '0')
                                try:
                                    value = float(value)
                                except (ValueError, TypeError):
                                    value = 0
                                data_series[category][item].append(value)

        self._cached_user_id = user_id
        self._cached_data = (dates, data_series)
        return dates, data_series

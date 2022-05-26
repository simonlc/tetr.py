import os, json, pygame

defaultSettings = {
  'DAS': 10,
  'ARR': 1,
  'Soft Drop': 1,
  'Sound': 100,
  'Music': 100,
  'Block Skin': 0,
  'Ghost': 0,
  'Outline': 0,
}

defaultControls = {
    'moveLeft': pygame.K_j,
    'moveRight': pygame.K_l,
    'moveDown': pygame.K_k,
    'hardDrop': pygame.K_SPACE,
    'rotRight': pygame.K_v,
    'rotLeft': pygame.K_c,
    'rot180': pygame.K_x,
    'holdPiece': pygame.K_LSHIFT,
    'pause': pygame.K_RETURN,
    'menu': pygame.K_ESCAPE,
}

def load_existing_save(saveFile):
    with open(os.path.join(saveFile), 'r+') as file:
        save = json.load(file)
    return save

def write_save(data):
    with open(os.path.join(os.getcwd(), 'config.json'), 'w') as file:
        json.dump(data, file)

def load_save():
    try:
        save = load_existing_save('config.json')
    except:
        save = create_save()
        write_save(save)

    print('save loaded', save)
    return save

def create_save():
    new_save = {
        'controls': defaultControls,
        'settings': defaultSettings,
    }

    return new_save

# setting = {
#   'DAS': list(range(31)),
#   'ARR': list(range(11)),
#   # Gravity: (function() {
#   #   var array = [];
#   #   array.push('Auto');
#   #   array.push('0G');
#   #   for (var i = 1; i < 64; i++) array.push(i + '/64G');
#   #   for (var i = 1; i <= 20; i++) array.push(i + 'G');
#   #   return array;
#   # })(),
#   # 'Soft Drop': (function() {
#   #   var array = [];
#   #   for (var i = 1; i < 64; i++) array.push(i + '/64G');
#   #   for (var i = 1; i <= 20; i++) array.push(i + 'G');
#   #   return array;
#   # })(),
#   'Lock Delay': list(range(101)),
#   'Size': ['Auto', 'Small', 'Medium', 'Large'],
#   'Sound': ['Off', 'On'],
#   'Volume': list(range(101)),
#   'Block': ['Shaded', 'Solid', 'Glossy', 'Arika', 'World'],
#   'Ghost': ['Normal', 'Colored', 'Off'],
#   'Grid': ['Off', 'On'],
#   'Outline': ['Off', 'On'],
# }

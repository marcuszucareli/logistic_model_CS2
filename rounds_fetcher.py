import pandas as pd
import undetected_chromedriver as uc
import time
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from info_to_get import search_parameters

def get_elements(driver, info, ckeck_length=True):
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, search_parameters[info]['path']
            ))
        )
    except:
        raise Exception(f'Timeout waiting for {info}')
    
    elements = driver.find_elements(
        By.CSS_SELECTOR, search_parameters[info]['path']
    )
    
    if ckeck_length and len(elements) == 0:
        raise Exception(f'Filter found no {info}')
    
    return elements


def get_element_attribute(element, info):
    
    attribute = search_parameters[info]['attribute']
    
    try:
        if attribute == 'text':
            return element.text
        else:
            return element.get_attribute(attribute)
    except:
        raise Exception(f"Error getting attrbute {attribute}")
    

df = pd.read_csv("matches_stats.csv")
matches_urls = df.links.to_list()

driver = uc.Chrome()

rounds = []
rounds_economy = []

i = 0
try:
    for match_url in matches_urls:

        teams = {}
        
        driver.get(match_url)

        # Get teams
        try:
            teams_elements = get_elements(driver, 'teams')
            for number, team in enumerate(teams_elements):
                try:
                    teams[f'team_{number+1}'] = get_element_attribute(
                        team,
                        'teams'
                    )
                except:
                    teams[f'team_{number+1}'] = None
        except:
            teams['team_1'] = None
            teams['team_2'] = None
        print('got teams!')
        # Get maps urls
        try:
            maps_elements = get_elements(driver, 'maps')
            maps_urls = [get_element_attribute(j, 'maps') for j in maps_elements]
        except:
            error_round = {
                'match_url': match_url,
                'error': True
            }

            rounds.append(error_round)
            continue
        print('got maps!')
        # Iterate over maps pages
        for map_url in maps_urls:

            driver.get(map_url)
            
            # Get map name
            try:
                map_name_elements = get_elements(driver, 'map_name')
                map_name = get_element_attribute(map_name_elements[0], 'map_name')
            except:
                error_round = {
                    'match_url': match_url,
                    'error': True
                }
                
                rounds.append(error_round)
                continue
            print(f'got {map_name}!')
            # Get rounds
            try:
                rounds_team_1 = driver.find_elements(
                    By.CSS_SELECTOR,
                    f"div.round-history-team-row img[alt='{teams['team_1']}'] ~ img[src*='/img/static/scoreboard/']"
                )
                rounds_team_2 = driver.find_elements(
                    By.CSS_SELECTOR,
                    f"div.round-history-team-row img[alt='{teams['team_2']}'] ~ img[src*='/img/static/scoreboard/']"
                )
            except Exception as e:
                print(e)
                continue

            for round_number, (image_1, image_2) in enumerate(\
                zip(rounds_team_1, rounds_team_2), 1):
                
                try:
                    WebDriverWait(driver, 30).until(
                        EC.presence_of_element_located((
                            By.CSS_SELECTOR,
                            f"div.round-history-team-row img[alt='{teams['team_1']}'] ~ img"
                        ))
                    )
                except:
                    raise Exception(f'Timeout waiting for teams rounds')
                
                image_1_source = get_element_attribute(image_1, 'rounds')
                image_2_source = get_element_attribute(image_2, 'rounds')
                
                # Check if it's a round
                if image_1_source.endswith('/emptyHistory.svg') and \
                    image_2_source.endswith('/emptyHistory.svg'):
                        continue
                
                # Get winner 0 for team_1 (home) and 1 for team_2 (away)
                if image_1_source.endswith('/emptyHistory.svg'):
                    winner = 1
                    win_type = image_2_source.split('/')[-1]
                else:
                    winner = 0
                    win_type = image_1_source.split('/')[-1]

                # Get sides 0 for CT and 1 for T
                match win_type:
                    case 'ct_win.svg':
                        team_1_side = 0 if winner == 0 else 1
                        team_2_side = 0 if winner == 1 else 1
                    case 'bomb_defused.svg':
                        team_1_side = 0 if winner == 0 else 1
                        team_2_side = 0 if winner == 1 else 1
                    case 'bomb_exploded.svg':
                        team_1_side = 1 if winner == 0 else 0
                        team_2_side = 1 if winner == 1 else 0
                    case 't_win.svg':
                        team_1_side = 1 if winner == 0 else 0
                        team_2_side = 1 if winner == 1 else 0
                    case 'stopwatch.svg':
                        team_1_side = 0 if winner == 0 else 1
                        team_2_side = 0 if winner == 1 else 1
                
                current_round = {
                    'match_url': match_url,
                    'error': False,
                    'team_1': teams['team_1'],
                    'team_2': teams['team_2'],
                    'map_name': map_name,
                    'winner': winner,
                    'win_type': win_type,
                    'team_1_side': team_1_side,
                    'team_2_side': team_2_side,
                    'round': round_number
                }
                rounds.append(current_round)
            print('got rounds!')
            # Iterate over economy
            economy_url = map_url.replace('/matches/', '/matches/economy/')
                
            driver.get(economy_url)
            
            # Get rounds
            try:
                rounds_team_1 = driver.find_elements(
                    By.CSS_SELECTOR,
                    f"tr.team-categories td.team:has(img[alt='{teams['team_1']}']) ~ td"
                )
                rounds_team_2 = driver.find_elements(
                    By.CSS_SELECTOR,
                    f"tr.team-categories td.team:has(img[alt='{teams['team_2']}']) ~ td"
                )
            except Exception as e:
                print(e)
                continue
            
            for current_round, (equipament_1, equipament_2) in enumerate(\
            zip(rounds_team_1, rounds_team_2), 1):
                
                equipament_value_1 = get_element_attribute(
                    equipament_1,
                    'equipament'
                ).replace('Equipment value: ', '')
                equipament_value_2 = get_element_attribute(
                    equipament_2,
                    'equipament'
                ).replace('Equipment value: ', '')
                economy_round = {
                    'match_url': match_url,
                    'error': False,
                    'map_name': map_name,
                    'equipament_1': equipament_value_1,
                    'equipament_2': equipament_value_2,
                    'round': current_round
                }
                
                rounds_economy.append(economy_round)
            
        i += 1
        print(f'Finished {i}')
        print(f'{matches_urls[i]}')
        print('--------------------------------------------------------------------')
        time.sleep(random.randint(3, 9))
        
except Exception as e:
    
    print(f'ERROR in match url: {matches_urls[i]}')
    print(f'{e}')
            
finally:
    driver.close
    driver.quit()

    df = pd.DataFrame(rounds)
    df.to_csv('rounds_stats.csv', index=False)

    df1=pd.DataFrame(rounds_economy)
    df1.to_csv('rounds_economy.csv', index=False)
    
    df_final = pd.merge(df, df1, 'inner', on=['match_url', 'map_name', 'round'])

    df_final.to_csv('full_rounds.csv')
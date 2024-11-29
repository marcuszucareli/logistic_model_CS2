search_parameters = {
    'teams': {
        'url': 'https://www.hltv.org/stats/matches/mapstatsid/{id}/{team}_1-vs-{team_2}',
        'path_type': 'css_selector',
        'path': 'table.stats-table.totalstats th.st-teamname.text-ellipsis',
        'attribute': 'text'
    }, 
    'maps': {
        'url': 'https://www.hltv.org/stats/matches/{id}/{team_1}-vs-{team_2}',
        'path_type': 'css_selector',
        'path': 'a.col.stats-match-map.standard-box.a-reset.inactive',
        'attribute': 'href'
    }, 
    'map_name': {
        'url': 'https://www.hltv.org/stats/matches/mapstatsid/{id}/{team_1}-vs-{team_2}',
        'path_type': 'css_selector',
        'path': 'a[class="col stats-match-map standard-box a-reset"] div.stats-match-map-result-mapname.dynamic-map-name-full',
        'attribute': 'text'
    },
    'rounds': {
        'url': 'https://www.hltv.org/stats/matches/mapstatsid/{id}/{team_1}-vs-{team_2}',
        'path_type': 'css_selector',
        'path': "div.round-history-team-row img[alt='{team_1}n'] ~ img",
        'attribute': 'src'
    },
    'equipament': {
        'url': 'https://www.hltv.org/stats/matches/economy/mapstatsid/{id}/{team_1}-vs-{team_2}',
        'path_type': 'css_selector',
        # 'path': "div.round-history-team-row img[alt='{team_1}n'] ~ img",
        'attribute': 'title'
    },
}
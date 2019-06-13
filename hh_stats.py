from words import vac_types, exp_types
import statistics


def get_stats_type(items):
    """ Собрать статистику по категориям вакансий"""
    vac_type_list_from = {}
    vac_type_list_to = {}
    for v in vac_types:
        vac_type_list_from[v[0]] = []
        vac_type_list_to[v[0]] = []
    for item in items:
        if item['vac_type'] == '':
            continue
        if item['from'] != '':
            vac_type_list_from[item['vac_type']].append(int(item['from']))
        if item['to'] != '':
            vac_type_list_to[item['vac_type']].append(int(item['to']))

    vac_type_stats_from = {}
    vac_type_stats_to = {}
    for v in vac_types:
        ind = v[0]
        if vac_type_list_from[ind]:
            vac_type_stats_from[ind] = {}
            vac_type_stats_from[ind]['max'] = max(vac_type_list_from[ind])
            vac_type_stats_from[ind]['min'] = min(vac_type_list_from[ind])
            vac_type_stats_from[ind]['median'] = statistics.median(vac_type_list_from[ind])
            vac_type_stats_from[ind]['samples'] = len(vac_type_list_from[ind])

        if vac_type_list_to[ind]:
            vac_type_stats_to[ind] = {}
            vac_type_stats_to[ind]['max'] = max(vac_type_list_to[ind])
            vac_type_stats_to[ind]['min'] = min(vac_type_list_to[ind])
            vac_type_stats_to[ind]['median'] = statistics.median(vac_type_list_to[ind])
            vac_type_stats_to[ind]['samples'] = len(vac_type_list_to[ind])

    return vac_type_stats_from, vac_type_stats_to


def get_stats_exp(items, vac_type=''):
    """ Собрать статистику по требуемому опыту """
    """ Входные параметры: список вакансий, тип вакансий """
    exp_list_from = {}
    exp_list_to = {}
    for v in exp_types:
        exp_list_from[v] = []
        exp_list_to[v] = []
    for item in items:
        if item['experience'] == '':
            continue
        if vac_type != '' and item['vac_type'] != vac_type:
            continue
        if item['from'] != '':
            exp_list_from[item['experience']].append(int(item['from']))
        if item['to'] != '':
            exp_list_to[item['experience']].append(int(item['to']))

    exp_stats_from = {}
    exp_stats_to = {}
    for v in exp_types:
        exp_stats_from[v] = {}
        exp_stats_to[v] = {}
        if exp_list_from[v]:
            exp_stats_from[v]['max'] = max(exp_list_from[v])
            exp_stats_from[v]['min'] = min(exp_list_from[v])
            exp_stats_from[v]['median'] = statistics.median(exp_list_from[v])
            exp_stats_from[v]['samples'] = len(exp_list_from[v])
        if exp_list_to[v]:
            exp_stats_to[v]['max'] = max(exp_list_to[v])
            exp_stats_to[v]['min'] = min(exp_list_to[v])
            exp_stats_to[v]['median'] = statistics.median(exp_list_to[v])
            exp_stats_to[v]['samples'] = len(exp_list_to[v])
    return exp_stats_from, exp_stats_to

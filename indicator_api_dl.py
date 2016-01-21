from census import Census
import pandas as pd
import os
import json

# api key
#pass year here if needed
c = Census('3d3ffd3a72cfa222ef938c3319be9dd6708dfe91')


def h(geog_type, table_name, geog_id=Census.ALL):
    '''
    supported geog_type's : ['county', 'house', 'senate']
    '''

    if (geog_id is not Census.ALL) and (type(geog_id) != str):
        raise ValueError('Invalid geog id, must be a str with code that matches census ID, ex: "001"')

    if geog_type == 'county':
        if (geog_id is not Census.ALL) and (int(geog_id) % 2 == 0):
            raise ValueError('Invalid geog id, county census codes are odd numbers only')
        return c.acs5.state_county(('NAME', table_name), '13', geog_id)

    elif geog_type == 'house':
        return c.acs5.state_house(('NAME', table_name), '13', geog_id)

    elif geog_type == 'senate':
        return c.acs5.state_senate(('NAME', table_name), '13', geog_id)
    else:
        raise ValueError('Invalid geog type')


def get_all_district_values_as_dataframe(numer_tables, denom_tables, geog_type):
    numer_dfs = [pd.DataFrame(h(geog_type, i, Census.ALL)) for i in numer_tables]
    denom_dfs = [pd.DataFrame(h(geog_type, i, Census.ALL)) for i in denom_tables]

    #convert index to str census code
    #convert to numeric so we can add values
    for num in numer_dfs:
        num.set_index(num.iloc[:,-1], inplace = True)
        num.iloc[:,0] = pd.to_numeric(num.iloc[:,0])

    for denom in denom_dfs:
        denom.set_index(num.iloc[:,-1], inplace = True)
        denom.iloc[:,0] = pd.to_numeric(denom.iloc[:,0])
    return pd.concat([i[j] for i, j in zip(numer_dfs, numer_tables)], axis = 1).sum(axis = 1) / pd.concat([i[j] for i, j in zip(denom_dfs, denom_tables)], axis = 1).sum(axis = 1)


def child_not_in_preschool(geog_type, geog_id):
    numer_tables = ['B14003_050E', 'B14003_022E']
    denom_tables = ['B14003_004E', 'B14003_013E', 'B14003_032E', 'B14003_041E', 'B14003_050E', 'B14003_022E']

    #if we want all values
    if geog_id == Census.ALL:
        return get_all_district_values_as_dataframe(numer_tables, denom_tables, geog_type)

    numer_value = sum([float(h(geog_type, i, geog_id)[0][i]) for i in numer_tables])
    denom_value = sum([float(h(geog_type, i, geog_id)[0][i]) for i in denom_tables])

    return (numer_value / denom_value)

def child_wout_health_ins(geog_type, geog_id):
    '''
    LIST OF NO HEALTH INSURANCE, ALL CHILDREN

    var[var.index.str.contains('B27001') & var.label.str.contains('No health insurance') & (
        var.label.str.contains('Margin') == False)].label
    var[var.index.str.contains('B27001') & (var.label.str.contains('health insurance') == False) & (
        var.label.str.contains('Margin') == False)].label
    '''
    # children without health insurance
    numer_tables = ['B27001_005E', 'B27001_008E', 'B27001_033E', 'B27001_036E']
    # all children
    denom_tables = ['B27001_003E', 'B27001_006E', 'B27001_031E', 'B27001_034E']

    #if we want all values
    if geog_id == Census.ALL:
        return get_all_district_values_as_dataframe(numer_tables, denom_tables, geog_type)

    numer_value = sum([float(h(geog_type, i, geog_id)[0][i]) for i in numer_tables])
    denom_value = sum([float(h(geog_type, i, geog_id)[0][i]) for i in denom_tables])

    return (numer_value / denom_value)

def child_with_public_health_ins(geog_type, geog_id):
    # children without health insurance
    numer_tables = ['B27003_004E', 'B27003_007E', 'B27003_032E', 'B27003_035E']
    # all children
    denom_tables = ['B27003_003E', 'B27003_006E', 'B27003_031E', 'B27003_034E']


    #if we want all values
    if geog_id == Census.ALL:
        return get_all_district_values_as_dataframe(numer_tables, denom_tables, geog_type)

    numer_value = sum([float(h(geog_type, i, geog_id)[0][i]) for i in numer_tables])
    denom_value = sum([float(h(geog_type, i, geog_id)[0][i]) for i in denom_tables])

    return (numer_value / denom_value)


def child_single_parent_home(geog_type, geog_id):
    # children in single parent homes
    numer_tables = ['B09002_008E']
    # all children
    denom_tables = ['B09002_001E']

    #if we want all values
    if geog_id == Census.ALL:
        return get_all_district_values_as_dataframe(numer_tables, denom_tables, geog_type)

    num_val = sum([float(h(geog_type, i, geog_id)[0][i]) for i in numer_tables])
    denom_val = sum([float(h(geog_type, i, geog_id)[0][i]) for i in denom_tables])

    return (num_val / denom_val)

def teens_no_school_work(geog_type, geog_id):
    '''
    LIST OF NUMERATOR, DENOM

    var[var.index.str.contains('B14005') & (var.label.str.contains('Margin') == False) & (
        var.label.str.contains('Not enrolled') & var.label.str.contains('Unemployed') | (
            var.label.str.contains('Not enrolled') & var.label.str.contains('Not in labor')))].index.tolist()
    '''

    # teens 16 - 19 not in school and not working
    numer_tables = ['B14005_010E',
                    'B14005_011E',
                    'B14005_014E',
                    'B14005_015E',
                    'B14005_024E',
                    'B14005_025E',
                    'B14005_028E',
                    'B14005_029E']
    # all children 16 - 19
    denom_tables = ['B14005_001E']

    #if we want all values
    if geog_id == Census.ALL:
        return get_all_district_values_as_dataframe(numer_tables, denom_tables, geog_type)

    numer_value = sum([float(h(geog_type, i, geog_id)[0][i]) for i in numer_tables])
    denom_value = sum([float(h(geog_type, i, geog_id)[0][i]) for i in denom_tables])

    return numer_value / denom_value

def hs_dropouts(geog_type, geog_id):
    # teens 16 - 19 not in school and not graduates
    numer_tables = ['B14005_012E',
                    'B14005_026E']
    # all children 16 - 19
    denom_tables = ['B14005_001E']

    #if we want all values
    if geog_id == Census.ALL:
        return get_all_district_values_as_dataframe(numer_tables, denom_tables, geog_type)

    numer_value = sum([float(h(geog_type, i, geog_id)[0][i]) for i in numer_tables])
    denom_value = sum([float(h(geog_type, i, geog_id)[0][i]) for i in denom_tables])

    return numer_value / denom_value


def educ_attn_hs(geog_type, geog_id):
    '''
    B15002 IS TABLE NAME
    '''
    numer_tables = ['B15002_011E', 'B15002_012E', 'B15002_013E', 'B15002_014E',
                    'B15002_015E', 'B15002_016E', 'B15002_017E', 'B15002_018E',
                    'B15002_028E', 'B15002_029E', 'B15002_030E', 'B15002_031E',
                    'B15002_032E', 'B15002_033E', 'B15002_034E', 'B15002_035E']

    denom_tables = ['B15002_001E']

    #if we want all values
    if geog_id == Census.ALL:
        return get_all_district_values_as_dataframe(numer_tables, denom_tables, geog_type)

    numer_value = sum([float(h(geog_type, i, geog_id)[0][i]) for i in numer_tables])
    denom_value = sum([float(h(geog_type, i, geog_id)[0][i]) for i in denom_tables])

    return numer_value / denom_value


def educ_attn_bs(geog_type, geog_id):
    '''
    B15002 IS TABLE NAME
    '''
    numer_tables = ['B15002_015E', 'B15002_016E', 'B15002_017E', 'B15002_018E',
                    'B15002_032E', 'B15002_033E', 'B15002_034E', 'B15002_035E']
    denom_tables = ['B15002_001E']

    #if we want all values
    if geog_id == Census.ALL:
        return get_all_district_values_as_dataframe(numer_tables, denom_tables, geog_type)
    numer_value = sum([float(h(geog_type, i, geog_id)[0][i]) for i in numer_tables])
    denom_value = sum([float(h(geog_type, i, geog_id)[0][i]) for i in denom_tables])

    return numer_value / denom_value


def child_pov(geog_type, geog_id):
    '''
    B17024 IS TABLE NAME
    '''

    numer_tables = [
        # under 6 year olds
        'B17024_003E', 'B17024_004E', 'B17024_005E',
        # 6 to 11 year olds
        'B17024_016E', 'B17024_017E', 'B17024_018E',
        # 12 to 17 year olds
        'B17024_029E', 'B17024_030E', 'B17024_031E'
    ]

    denom_tables = ['B17024_002E', 'B17024_015E', 'B17024_028E']

    #if we want all values
    if geog_id == Census.ALL:
        return get_all_district_values_as_dataframe(numer_tables, denom_tables, geog_type)

    numer_value = sum([float(h(geog_type, i, geog_id)[0][i]) for i in numer_tables])
    denom_value = sum([float(h(geog_type, i, geog_id)[0][i]) for i in denom_tables])


    return numer_value / denom_value


def child_pov2(geog_type, geog_id):
    '''
    B17001 IS TABLE NAME
    '''
    f = lambda x: 'B17001_00' + str(x) + 'E' if x - 10 < 0 else 'B17001_0' + str(x) + 'E'
    numer_tables = [f(x) for x in range(4, 10)] \
                   + [f(x) for x in range(18, 24)]

    denom_tables = [f(x) for x in range(4, 10)] \
                   + [f(x) for x in range(18, 24)] \
                   + [f(x) for x in range(33, 39)] \
                   + [f(x) for x in range(47, 53)]

    #if we want all values
    if geog_id == Census.ALL:
        return get_all_district_values_as_dataframe(numer_tables, denom_tables, geog_type)

    numer_value = sum([float(h(geog_type, i, geog_id)[0][i]) for i in numer_tables])
    denom_value = sum([float(h(geog_type, i, geog_id)[0][i]) for i in denom_tables])

    return numer_value / denom_value


def no_parent_in_labor_force(geog_type, geog_id):
    '''
    B23008 IS TABLE NAME
    '''
    f = lambda x: 'B23008_00' + str(x) + 'E' if x - 10 < 0 else 'B23008_0' + str(x) + 'E'
    numer_tables = [f(7), f(11), f(14), f(20), f(24), f(27)]
    denom_tables = [f(2), f(15)]

    #if we want all values
    if geog_id == Census.ALL:
        return get_all_district_values_as_dataframe(numer_tables, denom_tables, geog_type)

    numer_value = sum([float(h(geog_type, i, geog_id)[0][i]) for i in numer_tables])
    denom_value = sum([float(h(geog_type, i, geog_id)[0][i]) for i in denom_tables])
    return numer_value / denom_value


def fam_less_than_150(geog_type, geog_id):

    '''
    B17022 IS TABLE NAME
    '''
    f = lambda x: 'B17022_00' + str(x) + 'E' if x - 10 < 0 else 'B17022_0' + str(x) + 'E'
    numer_tables = [f(4), f(11), f(17), f(24), f(31), f(37)]
    denom_tables = [f(4), f(11), f(17), f(24), f(31), f(37), f(44), f(51), f(57), f(64), f(71), f(77)]

    #if we want all values
    if geog_id == Census.ALL:
        return get_all_district_values_as_dataframe(numer_tables, denom_tables, geog_type)

    numer_value = sum([float(h(geog_type, i, geog_id)[0][i]) for i in numer_tables])
    denom_value = sum([float(h(geog_type, i, geog_id)[0][i]) for i in denom_tables])
    return numer_value / denom_value



def homeownership(geog_type, geog_id):
    '''
    B25003 IS TABLE NAME
    '''
    numer_tables = ['B25003_002E']
    denom_tables = ['B25003_001E']

    #if we want all values
    if geog_id == Census.ALL:
        return get_all_district_values_as_dataframe(numer_tables, denom_tables, geog_type)

    else:
        numer_value = sum([float(h(geog_type, i, geog_id)[0][i]) for i in numer_tables])
        denom_value = sum([float(h(geog_type, i, geog_id)[0][i]) for i in denom_tables])
        return numer_value / denom_value

def high_poverty(county_id):
    # only support counties
    if (int(county_id) % 2 == 0):
            raise ValueError('Invalid geog id, county census codes are odd numbers only')
    '''
    Get tracts of >30% poverty for the county, then sum the child population for each of these tracts
    '''
    tract_poverty = c.acs5.state_county_tract(('NAME', 'B17001_002E'), '13', county_id, Census.ALL)
    tract_population = c.acs5.state_county_tract(('NAME', 'B17001_001E'), '13', county_id, Census.ALL)
    high_pov_tracts = []
    #get the tracts with high poverty in the county
    for pov, pop in zip(tract_poverty, tract_population):
        pov_value = float(pov['B17001_002E'])
        pop_value = float(pop['B17001_001E'])
        pct_in_pov = pov_value/pop_value
        if pct_in_pov > .3:
            high_pov_tracts.append(pov['tract'])

    #for those tracts, get the child population of the tract
    high_pov_child_population = []
    tract_child_population = c.acs5.state_county_tract(('NAME', 'B09001_001E'), '13', county_id, Census.ALL)
    for child_pop in tract_child_population:
        if child_pop['tract'] in high_pov_tracts:
            high_pov_child_population.append(float(child_pop['B09001_001E']))
    high_pov_num = sum(high_pov_child_population)

    #then divide it by the total population of the county
    high_pov_denom = float(h('county', 'B09001_001E', county_id)[0]['B09001_001E'])

    #if the numerator is 0, return 0, else return the value
    if high_pov_num == 0:
        return 0
    return high_pov_num/high_pov_denom

def str_fill(integer):
    s = str(integer)
    if len(s) < 3:
        s = s.zfill(3)
    return s


def coordinator_list(dist_type, dist_number):
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    collab = pd.read_excel(r'static\excel\coord_contact.xls', index_col=0)
    if dist_type == 'house':
        overlap = pd.read_csv(r'static\csv\house_overlap.csv', index_col=0)
    elif dist_type == 'senate':
        overlap = pd.read_csv(r'static\csv\senate_overlap.csv', index_col=0)
    else:
        raise ValueError('only senate and house are supported')
    l = []
    for ix, r in collab.ix[overlap[overlap.index == dist_number].county].iterrows():
        l.append("<b>{0}</b><br>{1}<br>{2} {3}<br>{4}<br>{5}".format(
            *[ix, r['name'], r.first_name, r.last_name, r.email, r.phone]))

    n = []
    for i in range(0, len(l), 2):
        try:
            n.append([l[i], l[i + 1]])
        except IndexError:
            n.append([l[i], ''])
    return n


def get_districts(county):
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    overlap = pd.read_csv(r'static\csv\county_overlap.csv', index_col=0)
    return overlap.ix[county, :][['dist_type', 'dist']].sort(['dist_type', 'dist']).values.tolist()


# funcs = {
#     "not_attend_preschool_rate": child_not_in_preschool,
#     "no_health_insurance_rate": child_wout_health_ins,
#     "not_school_not_work_rate": teens_no_school_work,
#     "educ_attain_25_hs_rate": educ_attn_hs,
#     "educ_attain_25_bach_rate": educ_attn_bs,
#     "child_poverty_saipe_rate": child_pov,
#     "no_parent_in_labr_force_rate": no_parent_in_labor_force,
#     "families_lt_150per_of_pov_rate": fam_less_than_150,
#     "owner_occupied_housing_rate": homeownership
# }

pkls =  {
    "not_attend_preschool_rate": 'child_not_in_preschool',
    "no_health_insurance_rate": 'child_wout_health_ins',
    "not_school_not_work_rate": 'teens_no_school_work',
    "educ_attain_25_hs_rate": 'educ_attn_hs',
    "educ_attain_25_bach_rate": 'educ_attn_bs',
    "child_poverty_saipe_rate": 'child_pov',
    "no_parent_in_labr_force_rate": 'no_parent_in_labor_force',
    "families_lt_150per_of_pov_rate": 'fam_less_than_150',
    "owner_occupied_housing_rate": 'homeownership'
}

indicator_descriptions = {
    "not_attend_preschool_rate": 'Children not attending pre-school (ages 3-4)',
    "no_health_insurance_rate": 'Children without health insurance',
    "not_school_not_work_rate": 'Teens not in school and not working (ages 16-19)',
    "educ_attain_25_hs_rate": 'Adults with high school diploma',
    "educ_attain_25_bach_rate": "Adults with Bachelor's degree or higher",
    "child_poverty_saipe_rate": 'Child poverty',
    "no_parent_in_labr_force_rate": 'Children living in families where no parent has full time year-round employment',
    "families_lt_150per_of_pov_rate": 'Families with annual incomes less than 150% of poverty level',
    "owner_occupied_housing_rate": 'Homeownership'
}

state_averages = {
    "not_attend_preschool_rate": '50.6%',
    "no_health_insurance_rate": '8.9%',
    "not_school_not_work_rate": '10.4%',
    "educ_attain_25_hs_rate": '85.0%',
    "educ_attain_25_bach_rate": '28.3%',
    "child_poverty_saipe_rate": '27.3%',
    "no_parent_in_labr_force_rate": '8.7%',
    "families_lt_150per_of_pov_rate": '32.7%',
    "owner_occupied_housing_rate": '64.2%'
}
# indicator_ways = {
#     "not_attend_preschool_rate": 'Supporting access to public and private pre-school is one way Collaboratives help children and their parents <strong>gain access to pre-school</strong>.  Promoting Quality Rated to improve child care quality is another community strategy.',
#     "no_health_insurance_rate": 'Collaboratives help expand <strong>access to health insurance for children</strong> by helping publicize the enrollment process and connecting families to medical providers.',
#     "not_school_not_work_rate": 'Promoting GED programs to help dropouts get a high school degree is one way Collaboratives <strong>support teens who are not in school and not working</strong>. Afterschool programs, mentoring programs, and job training programs are pathways to being a productive adult.',
#     "educ_attain_25_hs_rate": '84.4%',
#     "educ_attain_25_bach_rate": '27.8%',
#     "child_poverty_saipe_rate": '27.3%',
#     "no_parent_in_labr_force_rate": '8.2%',
#     "families_lt_150per_of_pov_rate": '31.1%',
#     "owner_occupied_housing_rate": '66.0%'
# }
#change directory to location of script
# abspath = os.path.abspath(__file__)
# dname = os.path.dirname(abspath)
# os.chdir(dname)

#build the pandas dfs for all the functions and save as pickles
# child_not_in_preschool('house', Census.ALL).to_pickle('static/pkl/child_not_in_preschool_house.pkl')
# child_wout_health_ins('house', Census.ALL).to_pickle('static/pkl/child_wout_health_ins_house.pkl')
# pd.to_pickle(teens_no_school_work('house', Census.ALL), 'static/pkl/teens_no_school_work_house.pkl')
# pd.to_pickle(educ_attn_hs('house', Census.ALL), 'static/pkl/educ_attn_hs_house.pkl')
# pd.to_pickle(educ_attn_bs('house', Census.ALL), 'static/pkl/educ_attn_bs_house.pkl')
# pd.to_pickle(child_pov('house', Census.ALL), 'static/pkl/child_pov_house.pkl')
# pd.to_pickle(no_parent_in_labor_force('house', Census.ALL), 'static/pkl/no_parent_in_labor_force_house.pkl')
# pd.to_pickle(fam_less_than_150('house', Census.ALL), 'static/pkl/fam_less_than_150_house.pkl')
# pd.to_pickle(homeownership('house', Census.ALL), 'static/pkl/homeownership_house.pkl')
#
# child_not_in_preschool('senate', Census.ALL).to_pickle('static/pkl/child_not_in_preschool_senate.pkl')
# child_wout_health_ins('senate', Census.ALL).to_pickle('static/pkl/child_wout_health_ins_senate.pkl')
# pd.to_pickle(teens_no_school_work('senate', Census.ALL), 'static/pkl/teens_no_school_work_senate.pkl')
# pd.to_pickle(educ_attn_hs('senate', Census.ALL), 'static/pkl/educ_attn_hs_senate.pkl')
# pd.to_pickle(educ_attn_bs('senate', Census.ALL), 'static/pkl/educ_attn_bs_senate.pkl')
# pd.to_pickle(child_pov('senate', Census.ALL), 'static/pkl/child_pov_senate.pkl')
# pd.to_pickle(no_parent_in_labor_force('senate', Census.ALL), 'static/pkl/no_parent_in_labor_force_senate.pkl')
# pd.to_pickle(fam_less_than_150('senate', Census.ALL), 'static/pkl/fam_less_than_150_senate.pkl')
# pd.to_pickle(homeownership('senate', Census.ALL), 'static/pkl/homeownership_senate.pkl')






# read the census variable description into a dataframe
#j = json.load(open('variables.json'))
#var = pd.DataFrame.from_dict(j['variables'], orient='index')
#var.label = var.label.str.replace('!!', ' ')

# get a list of state senate and house geog id's
# senate_geog_ids = [str(d['state legislative district (upper chamber)']) for d in h('senate', 'B01001_001E')]
# house_geog_ids = [str(d['state legislative district (lower chamber)']) for d in h('house', 'B01001_001E')]
#house_child_not_in_preschool = child_not_in_preschool('house', Census.ALL)

#county_geog_ids = {str(d['NAME'].split(' County, Georgia')[0]): str(d['county']) for d in h('county', 'B01001_001E')}

#tests
#t = child_not_in_preschool('county', county_geog_ids['Atkinson'])
#hi = child_wout_health_ins('county', county_geog_ids['Atkinson'])
#nw = teens_no_school_work('county', county_geog_ids['Atkinson'])
#bs = educ_attn_bs('county', county_geog_ids['Atkinson'])
#chpov = child_pov('county', county_geog_ids['Atkinson'])
#chpov2 = child_pov2('county', county_geog_ids['Atkinson'])
#nop = no_parent_in_labor_force('county', county_geog_ids['Atkinson'])
#fam = fam_less_than_150('county', county_geog_ids['Atkinson'])
#home = homeownership('county', county_geog_ids['Atkinson'])
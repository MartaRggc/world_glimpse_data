import pylab as plt
import seaborn as sns
import re
import pandas as pd
from fuzzywuzzy import fuzz
import sys
#sys.path.append('../src')

    
# Cleaning number function:

def clean_number(x):
    
    try:
        if '%' in x:
            return round(float(x.replace('%','').strip())/100,3) # Normalized rate
        else:
            return round(float(x.strip()),3) # Return float
        
    except:
        return x
    
    
    
# Changing country name function:

def to_proper_country_name(c):
    
    if c == 'United Kingdom':
        c = 'United Kingdom of Great Britain'
        
    elif c == 'Lao PDR' or c == 'Laos': 
        c = 'Lao People’s Democratic Republic'
        
    elif c == 'United Republic of Tanzania':
        c = 'Tanzania'
        
    elif c == 'North Korea' or c == 'DPRK':
        c = 'Democratic People’s Republic of Korea'
        
    elif c == 'South Korea':
        c = 'Republic of Korea'
        
    elif c == 'Ivory Coast':
        c = "Côte d'Ivoire"
        
    elif c == 'Russian Federation':
        c = 'Russia'
        
    elif c == 'United States':
        c = 'United States of America'
        
    elif c == 'East Timor':
        c = 'Timor-Leste'
        
    elif c == 'Turkey':
        c = 'Türkiye'
        
    elif c == 'Syria':
        c = 'Syrian Arab Republic'
        
    elif c == "China, People's Republic of":
        c = 'China'
        
    elif c == "Korea, Democratic People's Republic of":
        c = "Democratic People’s Republic of Korea"
        
    elif c == "Czechia":
        c = "Czech Republic"
        
    elif c == 'Tanzania (United Republic of)':
        c = 'Tanzania'
        
    elif c == "Korea (Democratic People's Rep. of)":
        c == "Democratic People’s Republic of Korea"
        
    elif c == "Federated States of Micronesia" or c == "Micronesia (Federal States of)":
        c == "Micronesia"
        
    else:
        pass
    
    reference_names = [
         
         'Micronesia',
         'Brunei',
         'Palestine',
         'Vatican City',
         'Iceland',
         'Norway',
         'Finland',
         'New Zealand',
         'Sweden',
         'Germany',
         'Nicaragua',
         'Namibia',
         'Lithuania',
         'Belgium',
         'Ireland',
         'Rwanda',
         'Latvia',
         'Costa Rica',
         'United Kingdom of Great Britain',
         'Philippines',
         'Albania',
         'Spain',
         'Moldova',
         'South Africa',
         'Switzerland',
         'Estonia',
         'Denmark',
         'Jamaica',
         'Australia',
         'Mozambique',
         'Chile',
         'Netherlands',
         'Slovenia',
         'Canada',
         'Barbados',
         'Portugal',
         'Mexico',
         'Peru',
         'Burundi',
         'Argentina',
         'Cabo Verde',
         'Serbia',
         'Liberia',
         'France',
         'Belarus',
         'Colombia',
         'United States of America',
         'Luxembourg',
         'Zimbabwe',
         'Eswatini',
         'Austria',
         'Tanzania',
         'Singapore',
         'Ecuador',
         'Madagascar',
         'Suriname',
         'Honduras',
         'Lao People’s Democratic Republic',
         'Bolivia',
         'Croatia',
         'Brazil',
         'Panama',
         'Bangladesh',
         'Poland',
         'Kazakhstan',
         'Armenia',
         'Slovakia',
         'Botswana',
         'Bulgaria',
         'Ukraine',
         'Uruguay',
         'El Salvador',
         'Montenegro',
         'Malta',
         'United Arab Emirates',
         'Viet Nam',
         'Macedonia',
         'Thailand',
         'Ethiopia',
         'Georgia',
         'Kenya',
         'Uganda',
         'Italy',
         'Mongolia',
         'Dominican Republic',
         'Lesotho',
         'Kyrgyzstan',
         'Israel',
         'Zambia',
         'Bosnia Herzegovina',
         'Romania',
         'Indonesia',
         'Belize',
         'Togo',
         'Paraguay',
         'Cambodia',
         'Greece',
         'Cameroon',
         'Timor-Leste',
         'Brunei Darussalam',
         'Azerbaijan',
         'Mauritius',
         'Hungary',
         'Ghana',
         'Czech Republic',
         'Malaysia',
         'Bhutan',
         'Senegal',
         'Republic of Korea',
         'Cyprus',
         'China',
         'Vanuatu',
         'Burkina Faso',
         'Malawi',
         'Tajikistan',
         'Sierra Leone',
         'Bahrain',
         'Comoros',
         'Sri Lanka',
         'Nepal',
         'Guatemala',
         'Angola',
         'Gambia',
         'Kuwait',
         'Fiji',
         'Myanmar',
         "Côte d'Ivoire",
         'Maldives',
         'Japan',
         'Jordan',
         'India',
         'Tunisia',
         'Türkiye',
         'Nigeria',
         'Saudi Arabia',
         'Lebanon',
         'Qatar',
         'Egypt',
         'Niger',
         'Morocco',
         'Guinea',
         'Benin',
         'Oman',
         'Congo',
         'Mali',
         'Pakistan',
         'Iran',
         'Algeria',
         'Chad',
         'Afghanistan',
         'Trinidad and Tobago',
         'Yemen',
         'Venezuela',
         'Uzbekistan',
         'Tuvalu',
         'Turkmenistan',
         'Tonga',
         'Syrian Arab Republic',
         'Sudan',
         'South Sudan',
         'Somalia',
         'Solomon Islands',
         'Seychelles',
         'Sao Tome and Principe',
         'San Marino',
         'Samoa',
         'Saint Vincent and the Grenadines',
         'Saint Lucia',
         'Saint Kitts and Nevis',
         'Russia',
         'Papua New Guinea',
         'Palau',
         'Nauru',
         'Monaco',
         'Mauritania',
         'Marshall Islands',
         'Liechtenstein',
         'Libya',
         'Kiribati',
         'Iraq',
         'Haiti',
         'Guyana',
         'Guinea-Bissau',
         'Grenada',
         'Gabon',
         'Eritrea',
         'Equatorial Guinea',
         'Djibouti',
         'Cuba',
         'Central African Republic',
         'Bahamas',
         'Antigua and Barbuda',
         'Andorra',
         'Dominica',
         "Democratic People’s Republic of Korea",
         
    ]
    
    def isolate(a):
        
        to_quit1 = ['republic',' united ',',','*','plurinational', 'kingdom of',
                   'islamic','state','states','bolivarian','(',')',
                   'commonwealth','federal','democratic','union','oriental',
                   'northern','r.','pdr',"’","'",'saint','czechia',
                   'north']
        
        to_quit2 = [' of ',' the',' and ',' dem. ',' rep. ',' the ',
                    'the ',' of', 'of ']
        
        a = a.lower()
        
        for i in to_quit1:
            a = a.replace(i,'')
            
        for i in to_quit2:
            a = a.replace(i,' ')
            
        return a.strip()
    
    
    similarity = [fuzz.ratio(isolate(i), isolate(c)) for i in reference_names]
    res = reference_names[similarity.index(max(similarity))]
    
    if max(similarity) > 70:
        return res   

    else:
        print(similarity.index(max(similarity)), c, res, f'max sim:{max(similarity)}') # to check
        return c + ' (country not in ref list)'
    

def change_to_country_id(clean_name):
    
    cc = pd.read_csv('../clean_data/countries.csv')
    
    try:
        return cc[cc.country_name == clean_name]['country_id'].iloc[0]
    
    except:
        return clean_name


def assign_region(countryid):
    
    cc = pd.read_csv('../clean_data/countries.csv')
    
    try:
        return cc[cc.country_id == countryid]['region_id'].iloc[0]
    
    except:
        return countryid
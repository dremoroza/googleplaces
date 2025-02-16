import streamlit as st
import pandas as pd
import json
import requests


key = json.loads(open('API_KEY.txt', 'r').read())
API_KEY = key['API-KEY']


#### Google Helper Functions
# Get postal areas / Latitudes and Longitudes using this function
def geocode_api(zipcode):
    lat, lng = None, None
#     api_key = GOOGLE_API_KEY
#     base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    base_url = f"https://maps.googleapis.com/maps/api/geocode/json?key={API_KEY}&components=postal_code:{zipcode}|country:US"

#     endpoint = f"{base_url}?address={address_or_zipcode}&key={api_key}"
    # see how our endpoint includes our API key? Yes this is yet another reason to restrict the key
    r = requests.get(base_url)
    if r.status_code not in range(200, 299):
        return None, None
    
    city_name = ''
    try:
        result = r.json()['results'][0]#['postcode_localities']
        
        city_name = [result['address_components'][el]['long_name']  for el in range(len(result['address_components'])) if 'locality' in result['address_components'][el]['types']][0]
        print(city_name) 
        localities = result['postcode_localities']
        
    except Exception as e:
        print(e)
        localities = None
    
    try:
        lat = result['geometry']['location']['lat']
        lng = result['geometry']['location']['lng']
    except: 
        lat, lng = None, None

    if localities is not None:
        # st.write(city_name)
        localities = [el for el in localities if city_name.lower() not in el.lower()]
        # st.write(localities)

    return localities, (lat, lng), city_name

########################################################################################

def get_places_df(url_query):

    if type(url_query) == str:
        print(url_query)
        r = requests.get(url_query)
        r = r.json()
        next_page_token = ''
        third_page_token = ''
        try:
            next_page_token = r['next_page_token']
        except:
            next_page_token = ''
        r = r['results']
        

        names_list = [r[el]['name'] for el in range(len(r))]
        rating = [r[el]['rating']  for el in range(len(r))]
        user_ratings_total = [r[el]['user_ratings_total'] for el in range(len(r))]
        address = [r[el]['formatted_address'] for el in range(len(r))]
        place_ids = [r[el]['place_id'] for el in range(len(r))]
        s_names_list = []
        s_rating = []
        s_user_ratings_total = []
        s_address = []
        s_place_ids = []
        t_names_list = []
        t_rating = []
        t_user_ratings_total = []
        t_address = []
        t_place_ids = []

        place_details_endpoint = 'https://maps.googleapis.com/maps/api/place/details/json'
        
        phone_numbers_list = []
        opening_hours_list = []
        place_urls = []
        s_phone_numbers_list = []
        s_opening_hours_list = []
        s_place_urls = []
        t_phone_numbers_list = []
        t_opening_hours_list = []
        t_place_urls = []

        for place_id in place_ids:
            dparams = {
                'key': 'AIzaSyDfyFnsTpBkfrC6vMvmAbnwxGENdWjIyYc',
                'placeid': place_id,
                'language': 'en'
            }
            r = requests.get(place_details_endpoint, params=dparams)
            r = r.json()  # See what we got
            r = r['result']
            
            try:
                place_phone_number = r['international_phone_number']
            except:
                place_phone_number = '-'
            try:
                opening_hours = '\n'.join(r['opening_hours']['weekday_text'])
            except: 
                opening_hours = '-'
            try:
                url = r['url']
            except:
                url = '-'
            
            phone_numbers_list.append(place_phone_number)
            opening_hours_list.append(opening_hours)
            place_urls.append(url)
        

        names_list = [str(el) for el in names_list]
        rating = [str(el) for el in rating]
        user_ratings_total = [str(el) for el in user_ratings_total]
        address = [str(el) for el in address]
        phone_numbers_list = [str(el) for el in phone_numbers_list]
        opening_hours_list = [str(el) for el in opening_hours_list]
        place_urls = [str(el) for el in place_urls]

        ## ---------seconda page --------####
        if next_page_token:
            second_page_url = url_query + "&pagetoken=" + next_page_token
            s = requests.get(second_page_url)
            s = s.json()
            try:
                 third_page_token = s['next_page_token']
            except:
                 third_page_token = ''
            s = s['results']
            

            s_names_list = [s[el]['name'] for el in range(len(s))]
            s_rating = [s[el]['rating']  for el in range(len(s))]
            s_user_ratings_total = [s[el]['user_ratings_total'] for el in range(len(s))]
            s_address = [s[el]['formatted_address'] for el in range(len(s))]
            s_place_ids = [s[el]['place_id'] for el in range(len(s))]

            place_details_endpoint = 'https://maps.googleapis.com/maps/api/place/details/json'
            
            s_phone_numbers_list = []
            s_opening_hours_list = []
            s_place_urls = []
            
            for place_id in s_place_ids:
                dparams = {
                    'key': 'AIzaSyDfyFnsTpBkfrC6vMvmAbnwxGENdWjIyYc',
                    'placeid': place_id,
                    'language': 'en'
                }
                s = requests.get(place_details_endpoint, params=dparams)
                s = s.json()  # See what we got
                s = s['result']
                
                try:
                    place_phone_number = s['international_phone_number']
                except:
                    place_phone_number = '-'
                try:
                    opening_hours = '\n'.join(s['opening_hours']['weekday_text'])
                except: 
                    opening_hours = '-'
                try:
                    url = s['url']
                except:
                    url = '-'
                
                s_phone_numbers_list.append(place_phone_number)
                s_opening_hours_list.append(opening_hours)
                s_place_urls.append(url)
            

            s_names_list = [str(el) for el in s_names_list]
            s_rating = [str(el) for el in s_rating]
            s_user_ratings_total = [str(el) for el in s_user_ratings_total]
            s_address = [str(el) for el in s_address]
            s_phone_numbers_list = [str(el) for el in s_phone_numbers_list]
            s_opening_hours_list = [str(el) for el in s_opening_hours_list]
            s_place_urls = [str(el) for el in s_place_urls]


        ## ---------third page --------####
        if third_page_token:
            third_page_url = url_query + "&pagetoken=" + third_page_token
            t = requests.get(third_page_url)
            t = t.json()
            t = t['results']
            

            t_names_list = [t[el]['name'] for el in range(len(t))]
            t_rating = [t[el]['rating']  for el in range(len(t))]
            t_user_ratings_total = [t[el]['user_ratings_total'] for el in range(len(t))]
            t_address = [t[el]['formatted_address'] for el in range(len(t))]
            t_place_ids = [t[el]['place_id'] for el in range(len(t))]

            place_details_endpoint = 'https://maps.googleapis.com/maps/api/place/details/json'
            
            t_phone_numbers_list = []
            t_opening_hours_list = []
            t_place_urls = []
            
            for place_id in t_place_ids:
                dparams = {
                    'key': 'AIzaSyDfyFnsTpBkfrC6vMvmAbnwxGENdWjIyYc',
                    'placeid': place_id,
                    'language': 'en'
                }
                t = requests.get(place_details_endpoint, params=dparams)
                t = t.json()  # See what we got
                t = t['result']
                
                try:
                    place_phone_number = t['international_phone_number']
                except:
                    place_phone_number = '-'
                try:
                    opening_hours = '\n'.join(t['opening_hours']['weekday_text'])
                except: 
                    opening_hours = '-'
                try:
                    url = t['url']
                except:
                    url = '-'
                
                t_phone_numbers_list.append(place_phone_number)
                t_opening_hours_list.append(opening_hours)
                t_place_urls.append(url)
            

            t_names_list = [str(el) for el in t_names_list]
            t_rating = [str(el) for el in t_rating]
            t_user_ratings_total = [str(el) for el in t_user_ratings_total]
            t_address = [str(el) for el in t_address]
            t_phone_numbers_list = [str(el) for el in t_phone_numbers_list]
            t_opening_hours_list = [str(el) for el in t_opening_hours_list]
            t_place_urls = [str(el) for el in t_place_urls]


        df = pd.DataFrame()
        df['Place'] = names_list + s_names_list + t_names_list
        df['Ratings'] = rating + s_rating + t_rating
        df['TotalRatings'] = user_ratings_total + s_user_ratings_total + t_user_ratings_total
        df['Address'] = address + s_address + t_address
        df['Phone Number'] = phone_numbers_list + s_phone_numbers_list + t_phone_numbers_list
        df['Opening Hours'] = opening_hours_list + s_opening_hours_list + t_opening_hours_list
        df['URL'] = place_urls + s_place_urls + t_place_urls
        return df

    else:

        all_names_list = []
        all_ratings_list = []
        all_user_ratings_total = []
        all_address = []
        all_phone_numbers = []
        all_opening_hours_list = []
        all_place_urls = []
        all_place_ids = []

        for query_ in url_query:
            r = requests.get(query_)
            r = r.json()
            next_page_token = ''
            third_page_token = ''
            try:
                next_page_token = r['next_page_token']
            except:
                 next_page_token = ''
            r = r['results']

            temp_names_list = [r[el]['name'] for el in range(len(r))]
            temp_rating = []
            temp_user_ratings_total = []

            for el in range(len(r)):
                try:
                    temp_rating.append(r[el]['rating'])
                except:
                    temp_rating.append('-')
                try:
                    temp_user_ratings_total.append(r[el]['user_ratings_total'])
                except:
                    temp_user_ratings_total.append('-')

            temp_address = [r[el]['formatted_address'] for el in range(len(r))]
            temp_place_ids = [r[el]['place_id'] for el in range(len(r))]

            names_list = []
            rating = []
            user_ratings_total = []
            address = []
            place_ids = []
            s_names_list = []
            s_rating = []
            s_user_ratings_total = []
            s_address = []
            s_place_ids = []
            t_names_list = []
            t_rating = []
            t_user_ratings_total = []
            t_address = []
            t_place_ids = []

            for el in range(len(temp_place_ids)):
                place_id = temp_place_ids[el]
                if place_id not in all_place_ids:
                    names_list.append(temp_names_list[el])
                    rating.append(temp_rating[el])
                    user_ratings_total.append(temp_user_ratings_total[el])
                    address.append(temp_address[el])
                    place_ids.append(temp_place_ids[el])


            place_details_endpoint = 'https://maps.googleapis.com/maps/api/place/details/json'
            
            phone_numbers_list = []
            opening_hours_list = []
            place_urls = []
            s_phone_numbers_list = []
            s_opening_hours_list = []
            s_place_urls = []
            t_phone_numbers_list = []
            t_opening_hours_list = []
            t_place_urls = []
            
            for place_id in place_ids:

                dparams = {
                    'key': 'AIzaSyDfyFnsTpBkfrC6vMvmAbnwxGENdWjIyYc',
                    'placeid': place_id,
                    'language': 'en'
                }
                r = requests.get(place_details_endpoint, params=dparams)
                r = r.json()  # See what we got
                r = r['result']
                
                try:
                    place_phone_number = r['international_phone_number']
                except:
                    place_phone_number = '-'
                try:
                    opening_hours = '\n'.join(r['opening_hours']['weekday_text'])
                except: 
                    opening_hours = '-'
                try:
                    url = r['url']
                except:
                    url = '-'
                
                phone_numbers_list.append(place_phone_number)
                opening_hours_list.append(opening_hours)
                place_urls.append(url)

            ################~~~~~~~~~~~ second    ~~~~~~~~~~~~~~############################
            if next_page_token:   
                second_page_url = query_ + "&pagetoken=" + next_page_token
                s = requests.get(second_page_url)
                s = s.json()
                try:
                    third_page_token = s['next_page_token']
                except:
                    third_page_token = ''
                s = s['results']

                s_temp_names_list = [s[el]['name'] for el in range(len(s))]
                s_temp_rating = []
                s_temp_user_ratings_total = []

                for el in range(len(s)):
                    try:
                        s_temp_rating.append(s[el]['rating'])
                    except:
                        s_temp_rating.append('-')
                    try:
                        s_temp_user_ratings_total.append(s[el]['user_ratings_total'])
                    except:
                        s_temp_user_ratings_total.append('-')

                s_temp_address = [s[el]['formatted_address'] for el in range(len(s))]
                s_temp_place_ids = [s[el]['place_id'] for el in range(len(s))]

                s_names_list = []
                s_rating = []
                s_user_ratings_total = []
                s_address = []
                s_place_ids = []

                for el in range(len(s_temp_place_ids)):
                    place_id = s_temp_place_ids[el]
                    if place_id not in all_place_ids:
                        s_names_list.append(s_temp_names_list[el])
                        s_rating.append(s_temp_rating[el])
                        s_user_ratings_total.append(s_temp_user_ratings_total[el])
                        s_address.append(s_temp_address[el])
                        s_place_ids.append(s_temp_place_ids[el])


                s_place_details_endpoint = 'https://maps.googleapis.com/maps/api/place/details/json'
                
                s_phone_numbers_list = []
                s_opening_hours_list = []
                s_place_urls = []
                
                for place_id in s_place_ids:

                    dparams = {
                        'key': 'AIzaSyDfyFnsTpBkfrC6vMvmAbnwxGENdWjIyYc',
                        'placeid': place_id,
                        'language': 'en'
                    }
                    s = requests.get(s_place_details_endpoint, params=dparams)
                    s = s.json()  # See what we got
                    s = s['result']
                    
                    try:
                        s_place_phone_number = s['international_phone_number']
                    except:
                        s_place_phone_number = '-'
                    try:
                        s_opening_hours = '\n'.join(s['opening_hours']['weekday_text'])
                    except: 
                        s_opening_hours = '-'
                    try:
                        s_url = s['url']
                    except:
                        s_url = '-'
                    
                    s_phone_numbers_list.append(s_place_phone_number)
                    s_opening_hours_list.append(s_opening_hours)
                    s_place_urls.append(s_url)    
            
            ################~~~~~~~~~~~ third    ~~~~~~~~~~~~~~############################
            if third_page_token:   
                third_page_url = query_ + "&pagetoken=" + third_page_token
                t = requests.get(third_page_url)
                t = t.json()
                t =  t['results']

                t_temp_names_list = [t[el]['name'] for el in range(len(t))]
                t_temp_rating = []
                t_temp_user_ratings_total = []

                for el in range(len(t)):
                    try:
                        t_temp_rating.append(t[el]['rating'])
                    except:
                        t_temp_rating.append('-')
                    try:
                        t_temp_user_ratings_total.append(t[el]['user_ratings_total'])
                    except:
                        t_temp_user_ratings_total.append('-')

                t_temp_address = [t[el]['formatted_address'] for el in range(len(t))]
                t_temp_place_ids = [t[el]['place_id'] for el in range(len(t))]

                t_names_list = []
                t_rating = []
                t_user_ratings_total = []
                t_address = []
                t_place_ids = []

                for el in range(len(t_temp_place_ids)):
                    place_id = t_temp_place_ids[el]
                    if place_id not in all_place_ids:
                        t_names_list.append(t_temp_names_list[el])
                        t_rating.append(t_temp_rating[el])
                        t_user_ratings_total.append(t_temp_user_ratings_total[el])
                        t_address.append(t_temp_address[el])
                        t_place_ids.append(t_temp_place_ids[el])


                t_place_details_endpoint = 'https://maps.googleapis.com/maps/api/place/details/json'
                
                t_phone_numbers_list = []
                t_opening_hours_list = []
                t_place_urls = []
                
                for place_id in t_place_ids:

                    dparams = {
                        'key': 'AIzaSyDfyFnsTpBkfrC6vMvmAbnwxGENdWjIyYc',
                        'placeid': place_id,
                        'language': 'en'
                    }
                    t = requests.get(t_place_details_endpoint, params=dparams)
                    t = t.json()  # See what we got
                    t = t['result']
                    
                    try:
                        t_place_phone_number = t['international_phone_number']
                    except:
                        t_place_phone_number = '-'
                    try:
                        t_opening_hours = '\n'.join(t['opening_hours']['weekday_text'])
                    except: 
                        t_opening_hours = '-'
                    try:
                        t_url = t['url']
                    except:
                        t_url = '-'
                    
                    t_phone_numbers_list.append(t_place_phone_number)
                    t_opening_hours_list.append(t_opening_hours)
                    t_place_urls.append(t_url)   



            all_names_list.extend(names_list + s_names_list + t_names_list)
            all_ratings_list.extend(rating + s_rating + t_rating)
            all_user_ratings_total.extend(user_ratings_total + s_user_ratings_total + t_user_ratings_total)
            all_address.extend(address + s_address + t_address)
            all_phone_numbers.extend(phone_numbers_list + s_phone_numbers_list + t_phone_numbers_list)
            all_opening_hours_list.extend(opening_hours_list  + s_opening_hours_list  + t_opening_hours_list )
            all_place_urls.extend(place_urls + s_place_urls + t_place_urls)
            all_place_ids.extend(place_ids + s_place_ids + t_place_ids)


        all_names_list = [str(el) for el in all_names_list]
        all_ratings_list = [str(el) for el in all_ratings_list]
        all_user_ratings_total = [str(el) for el in all_user_ratings_total]
        all_address = [str(el) for el in all_address]
        all_phone_numbers = [str(el) for el in all_phone_numbers]
        all_opening_hours_list = [str(el) for el in all_opening_hours_list]
        all_place_urls = [str(el) for el in all_place_urls]
        

        df = pd.DataFrame()
        df['Place'] = all_names_list
        df['Ratings'] = all_ratings_list
        df['TotalRatings'] = all_user_ratings_total
        df['Address'] = all_address
        df['Phone Number'] = all_phone_numbers
        df['Opening Hours'] = all_opening_hours_list
        df['URL'] = all_place_urls

        return df
######################################################################################################


def convert_df(df):
   return df.to_csv().encode('utf-8')



st.title("Google Maps Places Scraper")
st.subheader("Please enter input details below")

if 'submit' not in st.session_state:
    st.session_state['submit'] = ''

if 'places_df' not in st.session_state:
    st.session_state['places_df'] = ''


with st.expander("Input Form", expanded = True):
    form = st.form("Form")
    # form.warning('Please enter only any one of ZIP Code / Area. Do not enter both as it may produce incorrect results. Also, do not include any special characters like " , " (comma) , " . " (full-stop), etc.')
    zip_code = form.text_input("ZIP Code or Post Code:", help = "You can enter multiple ZIP Codes separated by a space between them, for example: 10001 10009")
    area = form.text_input("Area:", help = "Please enter the area in this format -> Area Name City Name")
    keyword = form.text_input("Search Keyword:")
    # negative_keyword = form.text_input("Negative Keyword:")
    submit = form.form_submit_button("Submit")


if submit:

    zip_code = str(zip_code)
    area = str(area).strip()

    if len(zip_code.strip()) != 0 and len(area.strip()) != 0:
        st.error('Please enter only any one of Area / ZIP Code.')

    elif len(zip_code.strip()) != 0:

        if len(zip_code.split()) == 1:
            localities, coordinates, city_name = geocode_api(zip_code)
            print(localities, coordinates, city_name)
            places_df = []

            if (localities == None) and (coordinates == (None, None)):
                st.error('🚨 Error: Cannot find Localities and Coordinates for given ZIP Code. Please try using a different ZIP.')


            if (localities == None) or (len(localities) == 0):
                
                latitude = coordinates[0]
                longitude = coordinates[1]

                print('LATITUDE:', latitude)

                # if negative_keyword.strip() == '':
                #     search_query = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={keyword}&location={latitude},{longitude}&key={API_KEY}"
                # else:
                #     search_query = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={keyword}-{negative_keyword}&location={latitude},{longitude}&key={API_KEY}"
                search_query = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={keyword}&location={latitude},{longitude}&key={API_KEY}"

                places_df = get_places_df(search_query)


            else:
                localities = ['+'.join(locality.split()) for locality in localities]
                query_list = [f"{keyword}+{locality}+{city_name}" for locality in localities]

                query_list = list(set([el.strip().lower() for el in query_list]))

                query_list = [f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key={API_KEY}" for query in query_list]

                places_df = get_places_df(query_list)

        else:

            all_query_list = []

            places_df = []

            for zip in zip_code.split():
                localities, coordinates, city_name = geocode_api(zip)

                if (localities == None) and (coordinates == (None, None)):
                    st.error(f'🚨 Error: Cannot find Localities and Coordinates for given ZIP Code: {zip}. Please try using a different ZIP.')

                if (localities == None) or (len(localities) == 0):
                    
                    latitude = coordinates[0]
                    longitude = coordinates[1]

                    print('LATITUDE:', latitude)

                    # if negative_keyword.strip() == '':
                    #     search_query = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={keyword}&location={latitude},{longitude}&key={API_KEY}"
                    # else:
                    #     search_query = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={keyword}-{negative_keyword}&location={latitude},{longitude}&key={API_KEY}"
                    search_query = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={keyword}&location={latitude},{longitude}&key={API_KEY}"

                    all_query_list.append(search_query)
                    # print('SEARCH QUERY:', search_query)
                    # places_df = get_places_df(search_query)


                else:
                    localities = ['+'.join(locality.split()) for locality in localities]

                    # if negative_keyword.strip() == "":
                    #     query_list = [f"{keyword}+{locality}+{city_name}" for locality in localities]
                    # else:
                    #     query_list = [f"{keyword}+{locality}+{city_name}" for locality in localities]
                    query_list = [f"{keyword}+{locality}+{city_name}" for locality in localities]
                    
                    query_list = list(set([el.strip().lower() for el in query_list]))

                    query_list = [f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key={API_KEY}" for query in query_list]

                    all_query_list.extend(query_list)
                    # places_df = get_places_df(query_list)
            print(all_query_list)
            places_df = get_places_df(all_query_list)

        
    else:

        area = '+'.join(area.split())
        query_input = f'{keyword}+{area}'

        query_url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query_input}&key={API_KEY}"

        places_df = get_places_df(query_url)

    try:
        st.write(places_df)

        csv = convert_df(places_df)

        st.download_button(

            label='📥 Download Current Result',
            data= csv,
            file_name= 'Scraped Places.csv'
        )

    except:
        pass

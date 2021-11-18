import pandas as pd
import numpy as np
import altair as alt

alt.data_transformers.disable_max_rows()

feature_name_map = {
    'methane_mixing_ratio_bias_corrected_mean': "Methane (ppb)",
    'reading_count': "Reading Count",
    'air_pressure_at_mean_sea_level_mean': "Sea Level Air Pressure (Pa)",
    'eastward_wind_at_100_metres_mean': "Eastward Wind (m/s)",
    'northward_wind_at_100_metres_mean': "Northward Wind (m/s)",
    'air_temperature_at_2_metres_mean': "Air Temperature (K)",
    'surface_air_pressure_mean': "Surface Air Pressure (Pa)",
    'integral_wrt_time_of_surface_direct_downwelling_shortwave_flux_in_air_1hour_Accumulation_mean': "Solar Radiation (J/m2)",
    'precipitation_amount_1hour_Accumulation_mean': "Precipitation (m)",
    'dew_point_temperature_at_2_metres_mean': "Dew Point Temperature (K)",
    'center_lat': "Center Latitude",
    'center_lon': "Center Longitude" 
}


def get_data_shape(df):
    return df.shape


def get_bar_zone_split(df_all):

    df_zone_split = df_all.groupby('BZone').size().reset_index().rename({0:"count"}, axis=1)
    df_zone_split['percent'] = df_zone_split['count']*100/ df_zone_split['count'].sum()
    df_zone_split = df_zone_split.rename({"BZone": "id", 
                  'count': 'reading_count',
                 }, axis=1).sort_values(by='id', ascending=True)
    zone_count_bar = alt.Chart(df_zone_split).mark_bar(tooltip=True).encode(y= alt.Y('id:N'),
                                                                        x= alt.X('percent:Q'),
                                                                        tooltip=['id', 'reading_count', 'percent'])

    return zone_count_bar.to_json()




def get_feature_dashboard(df_zone, cl_gdf, time_feature, bar_feature):
    
    
    zone_selector = alt.selection_multi(empty='all', fields=['BZone'])
    time_brush = alt.selection_interval(encodings=['x'])
    
    time_agg = 'mean'
    bar_agg = 'mean'    
    
    isSame = time_feature == bar_feature
    
    if isSame:
        
        if time_feature == 'reading_count':
            time_agg = 'sum'
        
        dt_zone_by_month = df_zone.set_index("time_utc").groupby([pd.Grouper(freq="M"), 'BZone']) \
                                                    .agg({time_feature: time_agg}) \
                                                    .reset_index() \
                                                    .rename({time_feature: feature_name_map[time_feature] + " " + time_agg.capitalize(),
                                                            }, axis=1)
                                                          
                                                          
        df_other = df_zone.set_index("time_utc").groupby([pd.Grouper(freq="M"), 'BZone']) \
                                                    .agg({bar_feature: bar_agg}) \
                                                    .reset_index() \
                                                    .rename({time_feature: feature_name_map[bar_feature] + " " + bar_agg.capitalize(),
                                                            }, axis=1)

        dt_zone_by_month[feature_name_map[bar_feature] + " " + bar_agg.capitalize()] = df_other[feature_name_map[bar_feature] + " " + bar_agg.capitalize()]
                                                          
        
    
    else:

        if time_feature =='reading_count':
            time_agg = 'sum'

        dt_zone_by_month = df_zone.set_index("time_utc").groupby([pd.Grouper(freq="M"), 'BZone']) \
                                                        .agg({time_feature: time_agg,
                                                              bar_feature: bar_agg}) \
                                                        .reset_index() \
                                                        .rename({time_feature: feature_name_map[time_feature],
                                                                 bar_feature: feature_name_map[bar_feature]
                                                                }, axis=1)
    
    
    dt_zone_by_month['time_utc'] = pd.to_datetime(dt_zone_by_month['time_utc'])

    time_suffix = " " + time_agg.capitalize() if isSame else ""
    bar_suffix = " " + bar_agg.capitalize() if isSame else ""
    
    
    #Scatter Plot for Zone Selection
    scatter_lat_lon = alt.Chart(cl_gdf[['rep_city', 'BZone', 'SHAPE_Area', 'center_lat', 'center_lon']], title="Zone Selection").mark_point(filled=True, size=200).encode(
                            x=alt.X('center_lon', title = feature_name_map['center_lon'], scale=alt.Scale(zero=False)),
                            y = alt.Y('center_lat', title= feature_name_map['center_lat'], scale=alt.Scale(zero=False)),
                            tooltip=['BZone','rep_city', 'center_lat', 'center_lon'],
                            color=alt.condition(zone_selector, 'BZone:N', alt.value('lightgray'), legend=None),
                        ).properties(
                            width = 250,
                            height = 300
                        ).add_selection(zone_selector)


    region_by_month = alt.Chart(dt_zone_by_month, title="Monthly " + feature_name_map[time_feature]).mark_line(
        point={
              "filled": False,
              "fill": "white"
            }
        ).encode(
            x='yearmonth(time_utc):O',
            y=alt.Y(f'{feature_name_map[time_feature] + time_suffix}:Q', title=f'{feature_name_map[time_feature]}', scale=alt.Scale(zero=False)),
            tooltip=['time_utc:O', f'{feature_name_map[time_feature] + time_suffix}:Q', 'BZone'],
            color=alt.condition(zone_selector | time_brush, 'BZone:N', alt.value('lightgray'), legend=None),
        ).transform_filter(
            zone_selector
        ).add_selection(zone_selector).add_selection(time_brush).properties(width=630)



    month_avg_bar = alt.Chart(dt_zone_by_month, title=f'Monthly Average {feature_name_map[bar_feature]}').mark_bar().encode(
        x = alt.X('BZone:N'),
        y = alt.Y(f'mean({feature_name_map[bar_feature] + bar_suffix}):Q', title=f'{feature_name_map[bar_feature]} Mean', scale=alt.Scale(zero=False)),
        tooltip=['BZone', f'mean({feature_name_map[bar_feature ]+ bar_suffix}):Q'],
        color=alt.condition(zone_selector, 'BZone:N', alt.value('lightgray'), legend=None),
    ).transform_filter(
            time_brush
    ).add_selection(zone_selector)


    chart = (scatter_lat_lon | month_avg_bar | region_by_month)        

    return chart.to_json()
        
        
        








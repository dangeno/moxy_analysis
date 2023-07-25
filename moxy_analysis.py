'''

Moxy Sensor Analysis
Canada Rowing

'''
import os
import fnmatch
import platform

import streamlit as st
import numpy as np 
import pandas as pd
import scipy as sp
import glob
import plotly.graph_objects as go
from datetime import datetime
import timedelta
from plotly.subplots import make_subplots
from scipy.signal import find_peaks
from scipy.signal import savgol_filter

import scipy.integrate as integrate

def format_date(date_str):
    # Define a mapping of month numbers to month names
    month_names = {
        '1': 'January',
        '2': 'February',
        '3': 'March',
        '4': 'April',
        '5': 'May',
        '6': 'June',
        '7': 'July',
        '8': 'August',
        '9': 'September',
        '10': 'October',
        '11': 'November',
        '12': 'December',
    }

    # Split the input date into month and day parts
    month, day = date_str.split('-')

    # Replace the month number with the corresponding name
    month_name = month_names.get(month, month)  # Use get() to handle invalid month numbers

    # Combine the month name and day and return the formatted date
    formatted_date = f"{month_name}-{day}"
    return formatted_date
st.image('rowing_canada.png', width = 150)
st.title("Rowing Canada Moxy Analysis")


uploaded_data = st.file_uploader('Selet Moxy Data')


fig = go.Figure()

if uploaded_data is not None:
	file = uploaded_data.name

	first = file.split('_')[1]
	last = file.split('_')[2]
	year = file.split('_')[3][0:4]


	data = pd.read_csv(uploaded_data, skiprows=3)
	sessions = data.groupby(['Session Ct']).count()
	sessions = sessions.index
	col1, col2 = st.columns(2)
	with col1:
		session = st.selectbox('Select Session', sessions)
	with col2: 
		data_sel = st.selectbox('Select Session', ['SmO2', 'THb', 'All Measures'])
	data = data.iloc[np.where(data['Session Ct']==session)[0],:]
	date = data['mm-dd'][0]
	date = format_date(date)
	

	Sm_avg = data['SmO2 Averaged']
	Sm_avg_max = Sm_avg[20:-20].max()

	Sm_live = data['SmO2 Live']
	Sm_live_max = Sm_avg[20:-20].max()
	
	THb = data['THb']
	THb_max = THb[20:-20].max()
	normalize = st.checkbox('Normalize Data to Max')
	if normalize is True:
		Sm_avg = Sm_avg/Sm_avg_max
		Sm_live = Sm_live/Sm_live_max
		THb = THb/THb_max

	if data_sel == 'SmO2':
		fig.add_trace(go.Scatter(y=Sm_avg,
			fill=None,
			mode='lines', 
			name = 'SmO2 Averaged'))
		fig.add_trace(go.Scatter(y=Sm_live,
			fill=None,
			mode='lines', 
			name = 'SmO2 Live'))
	elif data_sel == 'THb':
		fig.add_trace(go.Scatter(y=THb,
			fill=None,
			mode='lines', 
			name = 'THb'))
	elif data_sel == 'All Measures':
		fig.add_trace(go.Scatter(y=Sm_avg,
			fill=None,
			mode='lines', 
			name = 'SmO2 Averaged'))
		fig.add_trace(go.Scatter(y=Sm_live,
			fill=None,
			mode='lines', 
			name = 'SmO2 Live'))		
		fig.add_trace(go.Scatter(y=THb,
			fill=None,
			mode='lines', 
			name = 'THb'))
	fig.update_layout(
    	title=dict(text=f"<b>Moxy Sesnor Analysis</b> {first} {last} {date} {year}", font=dict(size=20)))
	fig.update_layout(xaxis_title = '<b>Sample Number</b>')
	fig.update_layout(yaxis_title = f'<b>{data_sel}</b>')



	st.plotly_chart(fig)
else: 
	st.header('Upload Data')
	st.stop()










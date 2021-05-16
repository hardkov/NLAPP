import streamlit as st

# -- Set page config
apptitle = 'NLAPP'
st.set_page_config(page_title=apptitle, page_icon=":tongue")

# -- Default detector list
detectorlist = ['H1','L1', 'V1']

# Title the app
st.title('Gravitational Wave Quickview')

st.markdown("""
 * Use the menu at left to select data and set plot parameters
 * Your plots will appear below
""")

st.sidebar.markdown("## Select Data Time and Detector")

#-- Set time by GPS or event
select_event = st.sidebar.selectbox('What is your name',
                                    ['Cris', 'Adam'])
    
#-- Choose detector as H1, L1, or V1
detector = st.sidebar.selectbox('Detector', detectorlist)

# -- Create sidebar for plot controls
st.sidebar.markdown('## Set Plot Parameters')
dtboth = st.sidebar.slider('Time Range (seconds)', 0.1, 8.0, 1.0)  # min, max, default
dt = dtboth / 2.0

st.sidebar.markdown('#### Whitened and band-passed data')
whiten = st.sidebar.checkbox('Whiten?', value=True)
freqrange = st.sidebar.slider('Band-pass frequency range (Hz)', min_value=10, max_value=2000, value=(30,400))


# -- Create sidebar for Q-transform controls
st.sidebar.markdown('#### Q-tranform plot')
vmax = st.sidebar.slider('Colorbar Max Energy', 10, 500, 25)  # min, max, default
qcenter = st.sidebar.slider('Q-value', 5, 120, 5)  # min, max, default
qrange = (int(qcenter*0.8), int(qcenter*1.2))

st.subheader('Raw data')
st.subheader('Whitened and Band-passed Data')

# -- Notes on whitening
st.header("jestem super nagłowek tekst koks")
with st.beta_expander("See notes"):
    st.markdown("""
 * Whitening is a process that re-weights a signal, so that all frequency bins have a nearly equal amount of noise. 
 * A band-pass filter uses both a low frequency cutoff and a high frequency cutoff, and only passes signals in the frequency band between these values.
See also:
 * [Signal Processing Tutorial](https://share.streamlit.io/jkanner/streamlit-audio/main/app.py)
""")


st.subheader('Q-transform')




with st.beta_expander("See notes"):

    st.markdown("""
A Q-transform plot shows how a signal’s frequency changes with time.
 * The x-axis shows time
 * The y-axis shows frequency
The color scale shows the amount of “energy” or “signal power” in each time-frequency pixel.
A parameter called “Q” refers to the quality factor.  A higher quality factor corresponds to a larger number of cycles in each time-frequency pixel.  
For gravitational-wave signals, binary black holes are most clear with lower Q values (Q = 5-20), where binary neutron star mergers work better with higher Q values (Q = 80 - 120).
See also:
 * [GWpy q-transform](https://gwpy.github.io/docs/stable/examples/timeseries/qscan.html)
 * [Reading Time-frequency plots](https://labcit.ligo.caltech.edu/~jkanner/aapt/web/math.html#tfplot)
 * [Shourov Chatterji PhD Thesis](https://dspace.mit.edu/handle/1721.1/34388)
""")


st.subheader("About this app")
st.markdown("""
This app displays data from LIGO, Virgo, and GEO downloaded from
the Gravitational Wave Open Science Center at https://gw-openscience.org .
You can see how this works in the [Quickview Jupyter Notebook](https://github.com/losc-tutorial/quickview) or 
[see the code](https://github.com/jkanner/streamlit-dataview).
""")
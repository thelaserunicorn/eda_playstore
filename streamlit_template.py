# 1 --- first and foremost, we import the necessary libraries
import pandas as pd
import numpy as np
import seaborn as sns
import streamlit as st

## copied from some random kaggle notebook (better visualization)
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import rcParams
import plotly.express as px
plt.style.use('ggplot')
rcParams['axes.spines.right'] = False
rcParams['axes.spines.top'] = False
rcParams['figure.figsize'] = [12, 9]
rcParams['font.size'] = 16
plt.rc('xtick', labelsize=12)
plt.rc('ytick', labelsize=12)
custom_colors = ['#74a09e','#86c1b2','#98e2c6','#f3c969','#f2a553', '#d96548', '#c14953']
sns.set_palette(custom_colors)

import warnings
warnings.filterwarnings('ignore')
#######################################





# 2 --- you can add some css to your Streamlit app to customize it
# TODO: Change values below and observer the changes in your app
st.markdown(
        f"""
<style>
    .reportview-container .main .block-container{{
        max-width: 90%;
        padding-top: 5rem;
        padding-right: 5rem;
        padding-left: 5rem;
        padding-bottom: 5rem;
    }}
    img{{
    	max-width:40%;
    	margin-bottom:40px;
    }}
</style>
""",
        unsafe_allow_html=True,
    )
#######################################






# 3 --- build the structure of your app


# Streamlit apps can be split into sections


# container -> horizontal sections
# columns -> vertical sections (can be created inside containers or directly in the app)
# sidebar -> a vertical bar on the side of your app


# here is how to create containers
header_container = st.container()
stats_container = st.container()	
viz_container = st.container()
st.set_option('deprecation.showPyplotGlobalUse', False)
#######################################



# You can place things (titles, images, text, plots, dataframes, columns etc.) inside a container
with header_container:

	# for example a logo or a image that looks like a website header

	# different levels of text you can include in your app
	st.title("Play Store Apps Data Analysis")
	st.markdown("This is a subset/chunk of a much larger data so results may vary significantly if full data is used")
	st.subheader("Top 5 Rows From The Dataset")


# Another container
with stats_container:


	# 4 --- You import datasets like you always do with pandas
	# 		if you'd like to import data from a database, you need to set up a database connection
	df = pd.read_csv('playstore_data.csv', nrows = 3000,  encoding= 'unicode_escape')
	lis = [x for x in range(-10,0)]
	df.drop(df.columns[lis], axis = 1, inplace = True)

	## replacing all category of games into one value = "Gaming"
	games = ["Card", "Casino", "Action" , "Trivia", "Puzzle", "Role Playing", "Racing", "Adventure", "Board", "Arcade", "Strategy", "Word"]

	for x in df.Category:
		if x in games:
			df.replace(x, 
			"Gaming", 
			inplace=True)
	
	content = ["Everyone 10+", "Everyone", "Unrated"]
	for y in df["Content Rating"]:
		if y in content:
			df.replace(y, 
			"Everyone", 
			inplace=True)

	#cleaning the values 

	df = df[df["Content Rating"] != "29-Oct-20"]
	df = df[df["Content Rating"] != "11-Nov-20"]
	df = df[df["Content Rating"] != "1-Nov-20"]
	df["Content Rating"].unique()

	st.write(df.head())
	st.write(df.describe())

	top_categories = [
    'Education', 'Music', 'Business', 'Tools', 
    'Entertainment', 'Lifestyle', 'Food & Drink', 
    'Books & Reference', 'Communication', 'Shopping', 'Gaming'
]

	top = df[df['Category'].isin(top_categories)].reset_index(drop=True)

with viz_container:

	st.subheader("Top Categories With Most Rating")
	x_cat_rev = top['Rating'].groupby(by = top['Category']).sum().sort_values(ascending =False)
	fig = px.histogram(x = x_cat_rev.index, y = x_cat_rev.values, color = x_cat_rev.index)
	st.plotly_chart(fig, use_container_width=True)

	st.subheader("Top Categories With Most Installs")
	x_val = top['Maximum Installs'].groupby(by = top['Category']).sum().sort_values(ascending =False)
	fig =px.bar(top, x = x_val.index, y = x_val, color = x_val.index)
	st.plotly_chart(fig, use_container_width=True)

	st.subheader("The Average Rating of each Category with over a Million Installs")
	million = top[top['Minimum Installs'] >= 1000000]
	average = million.groupby('Category')['Rating'].mean().sort_values(ascending=True)

	fig = px.bar(df, x=average, y=average.index, orientation='h', color=average.index, height=600)
	st.plotly_chart(fig, use_container_width=True)
	st.markdown("It can be argued that apps with over a million installs usually has an averate rating of 4 across all categories")

	st.subheader("Category with most apps")


	category_most_apps = df['Category'].value_counts().head(5)

	x3sis = []
	y3sis = []

	for i in range(len(category_most_apps)):
		x3sis.append(category_most_apps.index[i])
		y3sis.append(category_most_apps[i])

	fig = px.bar(x=x3sis,y=y3sis, color=x3sis)
	st.plotly_chart(fig)

	
	st.subheader("Boxplot of ratings of Top Categories")
	fig = px.box(x=top['Category'],y=top['Rating'], color=top['Category'])
	st.plotly_chart(fig)

	st.subheader("Average Rating Of Top Categories")
	x_rat_cat = top['Rating'].groupby(by = top['Category']).mean().sort_values(ascending =False)
	fig = px.bar(top, x=x_rat_cat.index, y = x_rat_cat.values, color = x_rat_cat)
	st.plotly_chart(fig)

	labels = df['Free'].value_counts(sort = True).index
	sizes = df['Free'].value_counts(sort = True)
	st.subheader("% of Free Apps and Paid Apps")
	fig = px.pie(df, values= sizes, names=["Free", "Paid"],  color_discrete_sequence=px.colors.sequential.Aggrnyl)
	st.plotly_chart(fig, use_container_width=True)
	st.markdown("According to the graph above, its clear that the number of reviews/ratings of free apps are generally higher compared to paid apps. Developer of paid apps can pursue the users to review their apps by using popups or other incentives. For example: developers of paid games can gift customers in-game currency if they review their apps. The impact of reviews is high and cannot be ignored as apps with higher reviews are prone to more downloads ")

	st.subheader("Comparison of Price of Paid Apps Between Categories")
	paid = top[top["Free"] == False]
	fig = px.box(paid, x="Category", y="Price", color="Category")
	st.plotly_chart(fig)

	st.subheader("Which are the categories with highest number of paid installations?")
	paid_cat_install = paid['Maximum Installs'].groupby(by = paid['Category']).sum().sort_values(ascending =False)
	fig = px.bar(paid, x = paid_cat_install.index, y = paid_cat_install.values , color =paid_cat_install)
	st.plotly_chart(fig, use_container_width=True)

	st.subheader("Which category with paid apps has highest ratings?")
	fig = px.bar(paid, x = paid['Rating'].groupby(by = paid['Category']).mean().sort_values().dropna().index, 
       y = paid['Rating'].groupby(by = paid['Category']).mean().sort_values().dropna().values,
       color = paid['Rating'].groupby(by = paid['Category']).mean().sort_values().dropna().index)
	st.plotly_chart(fig, use_container_width=True)

	install_cr = top['Category'].groupby(by = top['Content Rating']).count().sort_values(ascending =False)

	st.subheader("Which category of content rating contains most apps")
	fig = px.bar(top, x = install_cr.index, y = install_cr.values, color = install_cr.index)
	st.plotly_chart(fig)

	option = st.selectbox( 'Find top 10 apps of',  top_categories)
	def findtop10incategory(str):
		top10 = df[df['Category'] == str]
		top10apps = top10.sort_values(by='Maximum Installs', ascending=False).head(10)
   
		fig = px.bar(x = top10apps["App Name"], y = top10apps["Maximum Installs"], color=top10apps["App Name"])

		st.plotly_chart(fig)

	st.write(findtop10incategory(option))
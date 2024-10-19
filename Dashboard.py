import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html

import kagglehub

# Download latest version
path = kagglehub.dataset_download("mathchi/diabetes-data-set")

path= path+"\\Diabetes.csv"

df= pd.read_csv(path)


# Calculate metrics 
mean_glucose = df['Glucose'].mean()
mean_bmi = df['BMI'].mean()
DiabetesPedigreeFunction = df['DiabetesPedigreeFunction'].mean()
outcome_counts = df['Outcome'].value_counts()

bins=[20,30,40,60,82] 
labels=['Young ','Middle-Aged ','Older Adults','Seniors']
df["Agegroup"] = pd.cut(df["Age"].values, bins, right=False, labels=labels)

mean_bmi_by_agegroup = df.groupby(['Agegroup', 'Outcome'], observed= False)['BMI'].mean().unstack()
mean_diabetes_by_agegroup = df.groupby(['Agegroup', 'Outcome'], observed= False)['DiabetesPedigreeFunction'].mean().unstack()
mean_glucose_by_agegroup = df.groupby(['Agegroup', 'Outcome'],  observed= False)['Glucose'].mean().unstack()


app = Dash(__name__)


app.layout = html.Div([    
    html.H1("Diabetes Analysis Dashboard", style={'textAlign': 'center', 'fontSize': 50}),

    
    html.Div([
        html.Div(f"Mean Glucose: {mean_glucose:.2f}", style={'fontSize': 40, 'width': '20%', 'display': 'inline-block', 'textAlign': 'center'}),
        html.Div(f"Mean BMI: {mean_bmi:.2f}", style={'fontSize': 40, 'width': '20%', 'display': 'inline-block', 'textAlign': 'center'}),
        html.Div(f"Diabetes Function: {DiabetesPedigreeFunction:.2f}", style={'fontSize': 40, 'width': '20%', 'display': 'inline-block', 'textAlign': 'center'}),
        html.Div(f"Diabetes Cases: {outcome_counts[1]}", style={'fontSize': 40, 'width': '20%', 'display': 'inline-block', 'textAlign': 'center'}),
        html.Div(f"No Diabetes Cases: {outcome_counts[0]}", style={'fontSize': 40, 'width': '20%', 'display': 'inline-block', 'textAlign': 'center'}),
    ], style={'padding': '10px', 'textAlign': 'center', 'font-weight':'bold'}),

    
    html.Div([
        html.Div([
        html.Div(dcc.Graph(
        id='BMI-outcome',
        figure=go.Figure(
        data=[
            go.Bar(name='No Diabetes', x=mean_bmi_by_agegroup.index, y=mean_bmi_by_agegroup[0]),  # No Diabetes
            go.Bar(name='Diabetes', x=mean_bmi_by_agegroup.index, y=mean_bmi_by_agegroup[1])  # Diabetes
        ],
        layout=go.Layout(title='Mean BMI Levels by Age Group and Diabetes Outcome', barmode='group', font_size= 18)
        )
        ), style={'width': '50%', 'display': 'inline-block', 'height': '400px'}),  


        html.Div(dcc.Graph(
            id='Diabetes-outcome',
            figure=go.Figure(
            data=[
                go.Bar(name='No Diabetes', x=mean_diabetes_by_agegroup.index, y=mean_diabetes_by_agegroup[0]),  # No Diabetes
                go.Bar(name='Diabetes', x=mean_diabetes_by_agegroup.index, y=mean_diabetes_by_agegroup[1])  # Diabetes
                ],
            layout=go.Layout(title='Mean DiabetesPedigreeFunction by Category and Diabetes Outcome', barmode='group', font_size= 18))
            ), style={'width': '50%', 'display': 'inline-block', 'height': '400px'}),
        
        ], style={'display': 'flex', 'width': '50%'}), 

        html.Div(dcc.Graph(
            id='scatter-age-glucose',
            figure=go.Figure(
                data=go.Scatter(
                    x=df['Age'],
                    y=df['Glucose'],
                    mode='markers',
                    marker=dict(color=df['Outcome'], colorscale='Viridis', showscale=True),
                    text=df['Agegroup']
                ),
                layout=go.Layout(title='Age vs. Glucose', xaxis_title='Number of Pregnancies', yaxis_title='Glucose', font_size= 18)
            )
        ), style={'width': '50%', 'display': 'inline-block', 'height': '400px'}) 
    ], style={'display': 'flex', 'alignItems': 'flex-start'}),  

    html.Div([
        html.Div(dcc.Graph(
            id='Glucose-outcome',
            figure=go.Figure(
            data=[
                go.Bar(name='No Diabetes', x=mean_glucose_by_agegroup.index, y=mean_glucose_by_agegroup[0]),  # No Diabetes
                go.Bar(name='Diabetes', x=mean_glucose_by_agegroup.index, y=mean_glucose_by_agegroup[1])  # Diabetes
                ],
            layout=go.Layout(title='Mean Glucose by Category and Diabetes Outcome', barmode='group', font_size= 18))
            ), style={'width': '50%', 'display': 'inline-block', 'height': '400px'}),

        html.Div(dcc.Graph(
            id='outcome-pie-chart',
            figure=go.Figure(
                data=go.Pie(labels=['Diabetes', 'No Diabetes'], values=outcome_counts, hole=0.3),
                layout=go.Layout(title='Diabetes Outcome Distribution', font_size= 18)
            )
        ), style={'width': '50%', 'display': 'inline-block', 'height': '400px'}) 
    ], style={'display': 'flex', 'alignItems': 'flex-start'}), 

    html.Div(dcc.Graph(
        id='double-bar-chart',
        figure=go.Figure(
            data=[
                go.Bar(name='Pregnancies', x=df['Pregnancies'].value_counts().index, y=df['Pregnancies'].value_counts()),
                go.Bar(name='Diabetes', x=df['Pregnancies'].value_counts().index, y=df[df['Outcome'] == 1]['Pregnancies'].value_counts())
            ],
            layout=go.Layout(title='Double Bar Chart of Pregnancies vs. Diabetes Outcome', barmode='group',font_size= 18)
        )
    ), style={'width': '100%', 'display': 'inline-block', 'height': '250px'}), 
],  className="app")


if __name__ == '__main__':
    app.run_server(debug=True)
